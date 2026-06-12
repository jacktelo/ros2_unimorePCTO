import rclpy
from rclpy.node import Node
from more_interfaces.msg import AddressBook

class NodoA(Node):
    def __init__(self):
        super().__init__('nodo_a')
        self.pub = self.create_publisher(AddressBook, 'rubrica', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = AddressBook()
        msg.first_name = "Mario"
        msg.last_name = "Rossi"
        msg.phone_number = "3331234567"
        msg.phone_type = AddressBook.PHONE_TYPE_MOBILE

        self.pub.publish(msg)
        self.get_logger().info(
            f"Pubblicato: {msg.first_name} {msg.last_name} ({msg.phone_number}) [type={msg.phone_type}]"
        )

def main():
    rclpy.init()
    node = NodoA()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
