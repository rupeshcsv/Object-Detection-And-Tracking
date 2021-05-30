
import cv2

# read the video
cap = cv2.VideoCapture('cars_feed.mp4')

# Removing static background for motion detection
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=30)

while True:
	ret, frame = cap.read()

	# Region of interest - Only monitor a specific area of the video feed to count objects
	roi = frame[150:,:]

# Applying motion detection mask
	mask = object_detector.apply(roi)
	_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

	contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area > 200:
			# cv2.drawContours(roi, [cnt], -1, (255, 0, 0), 2)
			x, y, w, h = cv2.boundingRect(cnt)
			cv2.rectangle(roi, (x, y), (x+w, y+h), (255, 0, 0), 2)

	# display frame
	try:
		# cv2.imshow("ROI", roi)
		cv2.imshow("Mask applied on Region Of Interest", mask)
		cv2.imshow("Detection on Original Video", frame)
	except:
		pass

	key = cv2.waitKey(30)

	# 27 is Esc key on keyboard
	if key == 27:
		break

cap.release()
cv2.destroyAllWindows()
