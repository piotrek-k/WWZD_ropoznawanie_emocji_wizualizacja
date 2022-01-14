import os
import time
from pathlib import Path
from typing import Optional
from zipfile import ZipFile

import cv2
from fer import Video
from tqdm import tqdm

from fer.logger import log


class CustomizedVideo(Video):
    def analyze(
            self,
            detector,  # fer.FER instance
            display: bool = False,
            output: str = "csv",
            frequency: Optional[int] = None,
            max_results: int = None,
            save_fps: Optional[int] = None,
            video_id: Optional[str] = None,
            save_frames: bool = True,
            save_video: bool = True,
            annotate_frames: bool = True,
            zip_images: bool = True,
            detection_box: Optional[dict] = None
    ) -> list:
        """Recognize facial expressions in video using `detector`.

        Args:

            detector (fer.FER): facial expression recognizer
            display (bool): show images with cv2.imshow
            output (str): csv or pandas
            frequency (int): inference on every nth frame (higher number is faster)
            max_results (int): number of frames to run inference before stopping
            save_fps (bool): inference frequency = video fps // save_fps
            video_id (str): filename for saving
            save_frames (bool): saves frames to directory
            save_video (bool): saves output video
            annotate_frames (bool): add emotion labels
            zip_images (bool): compress output
            detection_box (dict): dict with bounding box for subimage (xmin, xmax, ymin, ymax)

        Returns:

            data (list): list of results

        """
        data = []
        if frequency is None:
            frequency = 1
        else:
            frequency = int(frequency)

        results_nr = 0

        # Open video
        assert self.cap.open(self.filepath), "Video capture not opening"
        self.__emotions = detector._get_labels().items()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        pos_frames = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        assert int(pos_frames) == 0, "Video not at index 0"

        frameCount = 0
        height, width = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        )

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        assert fps and length, "File {} not loaded".format(self.filepath)

        if save_fps is not None:
            frequency = fps // save_fps
            log.info("Saving every {} frames".format(frequency))

        log.info(
            "{:.2f} fps, {} frames, {:.2f} seconds".format(fps, length, length / fps)
        )

        capture_duration = 1000 / fps

        if save_frames:
            os.makedirs(self.outdir, exist_ok=True)
            log.info(f"Making directories at {self.outdir}")
        root, ext = os.path.splitext(os.path.basename(self.filepath))
        outfile = os.path.join(self.outdir, f"{root}_output{ext}")

        if save_video:
            videowriter = self._save_video(outfile, fps, width, height)

        pbar = tqdm(total=length, unit='frames')
        while self.cap.isOpened():
            start_time = time.time()
            ret, frame = self.cap.read()
            if not ret:  # end of video
                break
            if frameCount % frequency != 0:
                frameCount += 1
                continue

            if detection_box is not None:
                try:
                    frame = self._crop(frame, detection_box)
                except Exception as e:
                    log.error(e)
                    break

            padded_frame = detector.pad(frame)
            try:
                # Get faces with emotions
                faces = detector.detect_emotions(padded_frame)
                if detection_box is not None:
                    try:
                        for face in faces:
                            original_box = face.get("box")
                            face["box"] = (
                                original_box[0] + detection_box.get("x_min"),
                                original_box[1] + detection_box.get("y_min"),
                                original_box[2], original_box[3])
                            face["frame"] = frameCount
                    except Exception as e:
                        log.error(e)

            except Exception as e:
                log.error(e)
                break

            # Save images to `self.outdir`
            imgpath = os.path.join(
                self.outdir, (video_id or root) + str(frameCount) + ".jpg"
            )
            if save_frames and not annotate_frames:
                cv2.imwrite(imgpath, frame)

            if display or save_video or annotate_frames:
                assert isinstance(faces, list), type(faces)
                for face in faces:
                    bounding_box = face["box"]
                    emotions = face["emotions"]

                    cv2.rectangle(
                        frame,
                        (bounding_box[0] - 40, bounding_box[1] - 40),
                        (
                            bounding_box[0] - 40 + bounding_box[2],
                            bounding_box[1] - 40 + bounding_box[3],
                        ),
                        (0, 155, 255),
                        2,
                    )

                    for idx, (emotion, score) in enumerate(emotions.items()):
                        color = (211, 211, 211) if score < 0.01 else (0, 255, 0)
                        emotion_score = "{}: {}".format(
                            emotion, "{:.2f}".format(score) if score > 0.01 else ""
                        )
                        cv2.putText(
                            frame,
                            emotion_score,
                            (
                                bounding_box[0] - 40,
                                bounding_box[1] - 40 + bounding_box[3] + 30 + idx * 15,
                            ),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            color,
                            1,
                            cv2.LINE_AA,
                        )
                    if display:
                        cv2.imshow("Video", frame)
                    if save_frames and annotate_frames:
                        cv2.imwrite(imgpath, frame)
                    if save_video:
                        videowriter.write(frame)
                    results_nr += 1

                if display or save_video:
                    remaining_duration = max(
                        1, int((time.time() - start_time) * 1000 - capture_duration)
                    )
                    if cv2.waitKey(remaining_duration) & 0xFF == ord("q"):
                        break
                else:
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

            for f in faces:
                f["frame"] = frameCount

            frameCount += 1

            if faces:
                data.append(faces)
            if max_results and results_nr > max_results:
                break

            pbar.update(1)

        pbar.close()
        self.cap.release()
        if display or save_video:
            videowriter.release()
            if save_video:
                log.info(
                    "Completed analysis: saved to {}".format(self.tempfile or outfile)
                )
                if self.tempfile:
                    os.replace(self.tempfile, outfile)

        if save_frames and zip_images:
            log.info("Starting to Zip")
            outdir = Path(self.outdir)
            zip_dir = outdir / 'images.zip'
            images = sorted(list(outdir.glob("*.jpg")))
            total = len(images)
            i = 0
            with ZipFile(zip_dir, 'w') as zip:
                for file in images:
                    zip.write(file, arcname=file.name)
                    os.remove(file)
                    i += 1
                    if i % 50 == 0: log.info(f"Compressing: {i * 100 // total}%")
            log.info("Zip has finished")

        return data
