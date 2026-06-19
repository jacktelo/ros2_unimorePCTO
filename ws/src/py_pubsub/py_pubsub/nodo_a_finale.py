import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import os

class NodoA(Node):
    def __init__(self):
        super().__init__('nodo_a')
        
        # Bridge per convertire immagini OpenCV in messaggi ROS2
        self.bridge = CvBridge()
        
        # Sottoscrizione al trigger inviato da Nodo B
        self.trigger_sub = self.create_subscription(
            Bool,
            '/trigger',
            self.trigger_callback,
            10
        )
        
        # Publisher per lo streaming video diretto a Nodo B
        self.image_pub = self.create_publisher(
            Image,
            '/video_stream',
            10
        )
        
        # Percorso dell'immagine (condivisa tra Windows e Docker tramite il workspace)
        # Nello screen si trova dentro py_pubsub/py_pubsub/
        self.image_path = os.path.join(
            os.getcwd(), 'src', 'py_pubsub', 'py_pubsub', 'psyduck.jpg'
        )
        
        self.get_logger().info('Nodo A inizializzato e in ascolto del trigger...')

    def trigger_callback(self, msg):
        # Controlliamo se il trigger è True
        if msg.data:
            self.get_logger().info('Trigger ricevuto da Nodo B! Leggo l\'immagine da Windows...')
            
            if os.path.exists(self.image_path):
                # Carica l'immagine (simulando il frame della webcam salvato su disco)
                frame = cv2.imread(self.image_path)
                
                if frame is not None:
                    # Converte l'immagine OpenCV in messaggio ROS2 Image
                    ros_image = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                    # Pubblica l'immagine
                    self.image_pub.publish(ros_image)
                    self.get_logger().info('Immagine inviata con successo a Nodo B.')
                else:
                    self.get_logger().error('Errore nel caricamento del file immagine.')
            else:
                self.get_logger().error(f'File immagine non trovato in: {self.image_path}')

def main(args=None):
    rclpy.init(args=args)
    nodo_a = NodoA()
    try:
        rclpy.spin(nodo_a)
    except KeyboardInterrupt:
        pass
    finally:
        nodo_a.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()