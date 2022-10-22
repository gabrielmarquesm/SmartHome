import actuators_services_pb2 as pb
import actuators_services_pb2_grpc as pb_grpc


class ACService(pb_grpc.ACServicer):
    def __init__(self):
        self.power = True
        self.temperature = 20

    def to_celsius(self, tempFahrenheit):
        return (((tempFahrenheit - 32) * 5) / 9)

    def switchPower(self, request, context):
        self.power = not (self.power)
        msg = "O ar-condicionado está desligado"
        if self.power:
            msg = "O ar-condicionado está ligado"
        return pb.TempPowerStatus(status=msg)

    def changeTemperature(self, request, context):
        self.temperature = request.tempCelsius
        return pb.TempResponse(tempCelsius=self.temperature)

    # def convertReqResp(self, request, context):
    #     tempFahrenheit = request.tempFahrenheit
    #     print(f"Received tempRequest: {tempFahrenheit:.2f} F")
    #     tempCelsius = self.to_celsius(tempFahrenheit)
    #     print(f"Temperature in celsius: {tempCelsius:.2f} C")
    #     return actuators_services_pb2.TempResponse(tempCelsius=tempCelsius)
