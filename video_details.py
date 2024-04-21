
class VideoDetails:
	
	def __init__(self, video_title, person_list: Optional[List[Person]], processed_frames_list: Optional[List[Frame]]):
		self.video_title = video_title
		self.person_list = person_list
		self.IsProcessed = False
