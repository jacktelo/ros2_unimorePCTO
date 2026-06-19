import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class WebcamPublisher(Node):
    def __init__(self):
        super().__init__('nodo_a_webcam')
        self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
        
        # 10 FPS (0.1 secondi) per garantire stabilità totale
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.br = CvBridge()
        self.inizializza_webcam()

    def inizializza_webcam(self):
        self.get_logger().info("Inizializzazione webcam a risoluzione ridotta...")
        self.cap = cv2.VideoCapture(0)
        
        # 2. Imposta il formato dei pixel PRIMA della risoluzione (MJPEG o YUY2 alleggeriscono il flusso)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        
        # 3. Forza la risoluzione bassa (Risolve il timeout e il rettangolo verde)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        # 4. Buffer minimo per evitare lag e timeout
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not self.cap.isOpened():
            self.get_logger().error("Impossibile connettersi alla webcam!")
        else:
            self.get_logger().info("Webcam pronta a risoluzione ridotta!")

    def timer_callback(self):
        if not self.cap.isOpened():
            return

        # Svuota i buffer residui

        ret, frame = self.cap.read()
        
        if ret and frame is not None:
            # Mostra l'anteprima del Nodo A
            cv2.imshow("Finestra Video - Nodo A (Publisher)", frame)
            cv2.waitKey(1)
            
            # Pubblica il frame verso il Nodo B
            ros_image = self.br.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(ros_image)
        else:
            self.get_logger().warn('In attesa di dati stabili...')

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    nodo_a_webcam = WebcamPublisher()
    try:
        rclpy.spin(nodo_a_webcam)
    except KeyboardInterrupt:
        pass
    finally:
        nodo_a_webcam.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()