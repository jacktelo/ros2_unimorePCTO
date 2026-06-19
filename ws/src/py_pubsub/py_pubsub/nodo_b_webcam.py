import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class WebcamSubscriber(Node):
    def __init__(self):
        super().__init__('nodo_b_webcam')
        
        # Sottoscrizione al topic
        self.subscription = self.create_subscription(
            Image,
            'video_frames',
            self.listener_callback,
            10)
        self.subscription  # Evita warning
        
        self.br = CvBridge()
        self.get_logger().info('Nodo B avviato. In attesa di frame dal Nodo A...')

    def listener_callback(self, data):
        # Questo stamp di log ci serve per capire se il nodo sta ALMENO ricevendo i dati
        self.get_logger().info('Ricevuto un frame! Tento la visualizzazione...')
        
        try:
            # Converte il messaggio ROS2 in OpenCV
            current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')
            
            # Mostra il frame
            cv2.imshow("Webcam Stream - Nodo B", current_frame)
            
            # IMPORTANTE: Portiamo il waitKey a 10ms per dare tempo a Docker/WSL 
            # di elaborare la finestra grafica, altrimenti si blocca.
            cv2.waitKey(10)
            
        except Exception as e:
            self.get_logger().error(f'Errore durante la conversione o visualizzazione: {e}')

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    nodo_b_webcam = WebcamSubscriber()
    
    try:
        rclpy.spin(nodo_b_webcam)
    except KeyboardInterrupt:
        pass
    finally:
        nodo_b_webcam.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()