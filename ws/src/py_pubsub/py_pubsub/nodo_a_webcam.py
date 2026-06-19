import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class NodoBFinale(Node):
    def __init__(self):
        super().__init__('nodo_b_finale')
        
        # Inizializzazione del bridge per OpenCV
        self.bridge = CvBridge()
        
        # 1. Configurazione del Publisher per il Trigger
        self.trigger_pub = self.create_publisher(Bool, '/trigger', 10)
        
        # 2. Configurazione del Subscriber per lo streaming video
        self.image_sub = self.create_subscription(
            Image,
            '/video_stream',
            self.image_callback,
            10
        )
        
        # Timer per inviare il segnale di trigger ogni 2 secondi
        self.timer = self.create_timer(2.0, self.send_trigger)
        
        # Nome univoco per la finestra grafica di OpenCV
        self.window_name = "Streaming Video - Nodo B"
        
        self.get_logger().info('=== Nodo B Finale Avviato ===')
        self.get_logger().info('In attesa di immagini da mostrare a schermo...')

    def send_trigger(self):
        """Invia periodicamente il True per richiedere il frame al Nodo A."""
        msg = Bool()
        msg.data = True
        self.trigger_pub.publish(msg)
        self.get_logger().info('Trigger inviato al Nodo A.')

    def image_callback(self, msg):
        """
        Callback totalmente riscritto per la ricezione e la 
        visualizzazione immediata dell'immagine a schermo.
        """
        try:
            # Converte il messaggio ROS 2 in un'immagine OpenCV (matrice BGR)
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            
            # Apre la finestra pop-up e inserisce il frame corrente
            cv2.imshow(self.window_name, cv_image)
            
            # Forza l'ambiente grafico a renderizzare l'immagine e gestire la finestra (1 ms)
            cv2.waitKey(1)
            
            self.get_logger().info('Finestra grafica aggiornata con un nuovo frame!')
            
        except Exception as e:
            self.get_logger().error(f'Impossibile visualizzare il frame: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    nodo_b_finale = NodoBFinale()
    
    try:
        rclpy.spin(nodo_b_finale)
    except KeyboardInterrupt:
        nodo_b_finale.get_logger().info('Chiusura nodo interrotta da tastiera.')
    finally:
        # Distrugge in modo pulito tutte le finestre grafiche aperte da OpenCV
        cv2.destroyAllWindows()
        nodo_b_finale.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()