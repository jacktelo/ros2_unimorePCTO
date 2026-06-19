import rclpy
from rclpy.node import Node
from more_interfaces.msg import AddressBook


class NodoA(Node):

    def __init__(self):
        super().__init__('nodo_a')

        self.pub = self.create_publisher(AddressBook, 'topic_a', 10)
        self.sub = self.create_subscription(AddressBook, 'topic_b', self.callback, 10)

        self.count = 0
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = AddressBook()
        msg.first_name = "NodoA"
        msg.last_name = f"Periodic_{self.count}"
        msg.phone_number = "111111"
        msg.phone_type = AddressBook.PHONE_TYPE_WORK

        self.pub.publish(msg)
        self.get_logger().info(f"A → B (periodico): {msg.first_name} {msg.last_name}")
        self.count += 1
        self.timer.destroy()

    def callback(self, msg):
        self.get_logger().info(
            f"B → A (ricevuto): {msg.first_name} {msg.last_name} ({msg.phone_number}) type={msg.phone_type}"
        )

        risposta = AddressBook()
        risposta.first_name = "NodoA"
        risposta.last_name = "Risposta"
        risposta.phone_number = "222222"
        risposta.phone_type = AddressBook.PHONE_TYPE_HOME

        self.pub.publish(risposta)
        self.get_logger().info("A → B (risposta): Risposta inviata")


def main(args=None):
    rclpy.init(args=args)
    node = NodoA()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
