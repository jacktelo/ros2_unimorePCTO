import rclpy
from rclpy.node import Node
from more_interfaces.msg import AddressBook


class NodoB(Node):

    def __init__(self):
        super().__init__('nodo_b')

        self.pub = self.create_publisher(AddressBook, 'topic_b', 10)
        self.sub = self.create_subscription(AddressBook, 'topic_a', self.callback, 10)

        self.count = 0
        self.timer = self.create_timer(1.3, self.timer_callback)

    def timer_callback(self):
        msg = AddressBook()
        msg.first_name = "NodoB"
        msg.last_name = f"Periodic_{self.count}"
        msg.phone_number = "999999"
        msg.phone_type = AddressBook.PHONE_TYPE_MOBILE

        self.pub.publish(msg)
        self.get_logger().info(f"B → A (periodico): {msg.first_name} {msg.last_name}")
        self.count += 1

    def callback(self, msg):
        self.get_logger().info(
            f"A → B (ricevuto): {msg.first_name} {msg.last_name} ({msg.phone_number}) type={msg.phone_type}"
        )

        risposta = AddressBook()
        risposta.first_name = "NodoB"
        risposta.last_name = "Risposta"
        risposta.phone_number = "888888"
        risposta.phone_type = AddressBook.PHONE_TYPE_HOME

        self.pub.publish(risposta)
        self.get_logger().info("B → A (risposta): Risposta inviata")


def main(args=None):
    rclpy.init(args=args)
    node = NodoB()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
