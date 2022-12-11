import cv2
import os
import time
import hand as htm
import mediapipe as mp

ptime = 0
font = cv2.FONT_HERSHEY_PLAIN
cap = cv2.VideoCapture(0)
path = r"/media/binh/User/Pictures/finger"
list_img = os.listdir(path)
list_img_read = []
detector = htm.handDetector(detectionCon = 0.55)
for i in list_img:
	img = cv2.imread(f"{path}/{i}")
	list_img_read.append(img)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)




while True: 
	sucess , video = cap.read()

	ctime = time.time()
	fps = int(1/(ctime-ptime))
	cv2.putText(video, f"FPS:{fps}", (150,70), font, 3, (0,0,255), 3)
	ptime = ctime

	a = 0
	video = detector.findHands(video)
	lmlist = detector.findPosition(video, draw=False)
	if len(lmlist) == 21:
		if lmlist[6][2] < lmlist[8][2] and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
			a = 0
		if lmlist[6][2] > lmlist[8][2] and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
			a = 1
		if lmlist[6][2] > lmlist[8][2] and lmlist[10][2] > lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
			a = 2
		if lmlist[6][2] > lmlist[8][2] and lmlist[10][2] > lmlist[12][2] and lmlist[14][2] > lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
			a = 3
		if lmlist[6][2] > lmlist[8][2] and lmlist[10][2] > lmlist[12][2] and lmlist[14][2] > lmlist[16][2] and lmlist[18][2] > lmlist[20][2]:
			a = 4
		if lmlist[4][1] > lmlist[3][1] and lmlist[6][2] > lmlist[8][2]:
			a = 5

	width , height ,channel = list_img_read[a].shape
	video[:width,:height] = list_img_read[a]


	# imgRGB = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
	# results = faceMesh.process(imgRGB)
	# if results.multi_face_landmarks:
	# 	for faceLms in results.multi_face_landmarks:
	# 	    mpDraw.draw_landmarks(video, faceLms, mpFaceMesh.FACEMESH_TESSELATION,
	# 		drawSpec,drawSpec)
	# 	for id,lm in enumerate(faceLms.landmark):
	# 	    #print(lm)
	# 		ih, iw, ic = video.shape
	# 		x,y = int(lm.x*iw), int(lm.y*ih)
	# 		print(id,x,y)



	cv2.rectangle(video, (0,200), (200,400),(0,255,0))
	cv2.putText(video, f"{a}", (30,370), font, 15, (0,0,255), 4)

	cv2.imshow("video", video)
	if cv2.waitKey(1) == ord("q"):
		break 