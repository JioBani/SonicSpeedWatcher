class PassData:

  def __init__(self , exitTime, passingTime, velocity , imagePath) :
    self.exitTime = exitTime
    self.passingTime = passingTime
    self.velocity = velocity
    self.imagePath = imagePath

  def print(self) :
    print("퇴장 시각 : %f" % self.exitTime)
    print("통과 시간 : %f" % self.passingTime)
    print("평균 속도 : %f" % self.velocity)
    print("이미지 : %s " % self.imagePath)