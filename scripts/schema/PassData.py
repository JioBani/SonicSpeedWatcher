class PassData:

  def __init__(self , exitTime, passingTime, velocity) :
    self.exitTime = exitTime
    self.passingTime = passingTime
    self.velocity = velocity

  def print(self) :
    print("퇴장 시각 : %f" % self.exitTime)
    print("통과 시간 : %f" % self.passingTime)
    print("평균 속도 : %f" % self.velocity)