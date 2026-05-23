import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

ARQUIVO = '/mnt/c/Users/joaop/Documents/Projetos Inteli/Modulo 6/Ponderada ROS/caminho_tartaruga.txt'
LARGURA_CANETA = 1  # padrão do turtlesim é 3


class ControladorTartaruga(Node):
    def __init__(self):
        super().__init__('controlador_tartaruga')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.mover, 10)
        self.caminho = np.loadtxt(ARQUIVO, delimiter=',').tolist()
        self._ajustar_caneta()

    def _ajustar_caneta(self):
        cli = self.create_client(SetPen, '/turtle1/set_pen')
        if not cli.wait_for_service(timeout_sec=5.0):
            self.get_logger().warn('Serviço /turtle1/set_pen indisponível')
            return
        req = SetPen.Request()
        req.r, req.g, req.b = 255, 255, 255
        req.width = LARGURA_CANETA
        req.off = 0
        cli.call_async(req)

    def mover(self, pose):
        if not self.caminho:
            self.pub.publish(Twist())
            return

        x_alvo, y_alvo = self.caminho[0]
        dx, dy = x_alvo - pose.x, y_alvo - pose.y
        distancia = np.hypot(dx, dy)

        if distancia < 0.2:
            self.caminho.pop(0)
            return

        # Erro angular normalizado para (-pi, pi) → escolhe o giro mais curto
        diff = np.arctan2(dy, dx) - pose.theta
        erro_angulo = np.arctan2(np.sin(diff), np.cos(diff))

        cmd = Twist()
        cmd.angular.z = float(6.0 * erro_angulo)
        # Só avança quando já está alinhado — evita arcos no desenho
        if abs(erro_angulo) < 0.5:
            cmd.linear.x = float(2.0 * distancia)
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(ControladorTartaruga())
    rclpy.shutdown()


if __name__ == '__main__':
    main()
