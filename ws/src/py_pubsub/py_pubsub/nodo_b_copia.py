import rclpy
from rclpy.node import Node
from more_interfaces.msg import AddressBook

class NodoB(Node):
    def __init__(self):
        super().__init__('nodo_b')
        self.sub = self.create_subscription(
            AddressBook,
            'rubrica',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        phone_type_str = self.phone_type_to_string(msg.phone_type)

        self.get_logger().info(
            f"Ricevuto contatto: {msg.first_name} {msg.last_name} "
            f"- {msg.phone_number} ({phone_type_str})"
        )

    def phone_type_to_string(self, t):
        if t == AddressBook.PHONE_TYPE_HOME:
            return "HOME"
        if t == AddressBook.PHONE_TYPE_WORK:
            return "WORK"
        if t == AddressBook.PHONE_TYPE_MOBILE:
            return "MOBILE"
        return "UNKNOWN"

def main():
    rclpy.init()
    node = NodoB()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
