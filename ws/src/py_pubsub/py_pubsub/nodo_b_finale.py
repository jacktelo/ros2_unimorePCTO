import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os

class NodoB(Node):
    def __init__(self):
        super().__init__('nodo_b')
        self.bridge = CvBridge()
        
        # Publisher del trigger per attivare Nodo A
        self.trigger_pub = self.create_publisher(Bool, '/trigger', 10)
        
        # Sottoscrizione allo streaming video da Nodo A
        self.image_sub = self.create_subscription(
            Image,
            '/video_stream',
            self.image_callback,
            10
        )
        
        # Timer per inviare il trigger ogni 2 secondi
        self.timer = self.create_timer(2.0, self.send_trigger)
        
        # Percorso di salvataggio dell'output
        self.output_path = os.path.join(
            os.getcwd(), 'src', 'py_pubsub', 'py_pubsub', 'risultato_comunicazione.jpg'
        )
        
        self.get_logger().info('Nodo B inizializzato. Avvio invio trigger temporizzato...')

    def send_trigger(self):
        msg = Bool()
        msg.data = True
        self.trigger_pub.publish(msg)
        self.get_logger().info('Inviato segnale di trigger a Nodo A.')

    def image_callback(self, msg):
        self.get_logger().info('Immagine ricevuta da Nodo A!')
        try:
            # Converte il messaggio ROS2 in immagine OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            
            # Salva l'immagine sul Workspace condiviso (sarà visibile su Windows)
            cv2.imwrite(self.output_path, cv_image)
            self.get_logger().info(f'Immagine salvata in: {self.output_path}')
            
        except Exception as e:
            self.get_logger().error(f'Errore nella conversione dell\'immagine: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    nodo_b = NodoB()
    try:
        rclpy.spin(nodo_b)
    except KeyboardInterrupt:
        pass
    finally:
        nodo_b.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()