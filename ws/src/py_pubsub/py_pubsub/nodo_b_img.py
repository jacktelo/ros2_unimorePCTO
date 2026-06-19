import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String  # Per inviare la risposta di testo
import cv2
import numpy as np

class NodoB(Node):

    def __init__(self):
        super().__init__('nodo_b_listener_talker')
        
        # 1. LISTENER: Ascolta la foto dal Nodo A
        self.subscriber_foto = self.create_subscription(
            Image, 'topic_foto', self.foto_callback, 10)
        
        # 2. TALKER: Risponde al Nodo A con del testo
        self.publisher_risposta = self.create_publisher(String, 'topic_risposta', 10)
        
        self.get_logger().info('Nodo B pronto per il botta e risposta!')

    def foto_callback(self, msg):
        # Ricevo la foto dal Nodo A
        self.get_logger().info(f"<-- [Nodo B] Ricevuta foto {msg.width}x{msg.height} dal Nodo A!")
        
        try:
            # Opzionale: Mostra la finestra video (se l'ambiente lo supporta)
            img_array = np.frombuffer(msg.data, dtype=np.uint8)
            cv_image_rgb = img_array.reshape((msg.height, msg.width, 3))
            cv_image_bgr = cv2.cvtColor(cv_image_rgb, cv2.COLOR_RGB2BGR)
            cv2.imshow("Finestra Nodo B", cv_image_bgr)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Errore visualizzazione: {str(e)}")

        # "Risposta": Creo il messaggio di testo e lo rispedisco indietro subito
        risposta = String()
        risposta.data = f"Foto da {msg.width}x{msg.height} px ricevuta forte e chiaro!"
        
        self.publisher_risposta.publish(risposta)
        self.get_logger().info(f"--> [Nodo B] Inviata conferma di ricezione al Nodo A.")


def main(args=None):
    rclpy.init(args=args)
    node = NodoB()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()