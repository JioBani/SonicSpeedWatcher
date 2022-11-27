class PassData:

  def __init__(self ,
               exitTime,
               passingTime,
               velocity ,
               imagePath,
               isSpeeding
               ) :
    self.exitTime = exitTime
    self.passingTime = passingTime
    self.velocity = velocity
    self.imagePath = imagePath
    self.isSpeeding = isSpeeding

  def print(self) :
    print("퇴장 시각 : %f" % self.exitTime)
    print("통과 시간 : %f" % self.passingTime)
    print("평균 속도 : %f" % self.velocity)
    print("이미지 : %s " % self.imagePath)
    print("과속 {0}".format(self.isSpeeding))