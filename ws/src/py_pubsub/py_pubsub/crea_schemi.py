import cv2
import numpy as np

def crea_schema_trigger():
    # Crea uno sfondo scuro (stile tech)
    img = np.ones((600, 800, 3), dtype=np.uint8) * 20
    
    # Colori
    teal = (218, 255, 100) # #64ffda (BGR)
    white = (245, 245, 245)
    gray = (150, 150, 150)
    
    # Titolo
    cv2.putText(img, "NODO A - Versione Trigger", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, teal, 2)
    
    # Rettangolo 1
    cv2.rectangle(img, (150, 120), (650, 200), teal, 2)
    cv2.putText(img, "1. SUBSCRIBER (/trigger)", (170, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.7, white, 2)
    cv2.putText(img, "In ascolto del comando bool da Nodo B", (170, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    
    # Freccia 1
    cv2.arrowedLine(img, (400, 200), (400, 260), teal, 2, tipLength=0.3)
    cv2.putText(img, "Riceve True", (415, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, teal, 1)
    
    # Rettangolo 2
    cv2.rectangle(img, (150, 260), (650, 340), teal, 2)
    cv2.putText(img, "2. OPENCV (Lettura)", (170, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.7, white, 2)
    cv2.putText(img, "Carica psyduck.jpg da Volume Condiviso", (170, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    
    # Freccia 2
    cv2.arrowedLine(img, (400, 340), (400, 400), teal, 2, tipLength=0.3)
    cv2.putText(img, "CvBridge Convert", (415, 380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, teal, 1)
    
    # Rettangolo 3
    cv2.rectangle(img, (150, 400), (650, 480), teal, 2)
    cv2.putText(img, "3. PUBLISHER (/video_stream)", (170, 435), cv2.FONT_HERSHEY_SIMPLEX, 0.7, white, 2)
    cv2.putText(img, "Invia il frame ROS2 Image a Nodo B", (170, 465), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    
    cv2.imwrite('schema_trigger.png', img)
    print("Immagine 'schema_trigger.png' creata con successo!")

def crea_schema_timer():
    img = np.ones((500, 900, 3), dtype=np.uint8) * 20
    teal = (218, 255, 100)
    white = (245, 245, 245)
    gray = (150, 150, 150)
    
    cv2.putText(img, "NODO A - Versione Timer (Botta & Risposta)", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, teal, 2)
    
    # Rettangolo 1 (Top Left)
    cv2.rectangle(img, (50, 120), (420, 200), teal, 2)
    cv2.putText(img, "1. TIMER (Ogni 2s)", (70, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.7, white, 2)
    cv2.putText(img, "Si attiva ciclicamente", (70, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    
    # Freccia verso il basso
    cv2.arrowedLine(img, (235, 200), (235, 270), teal, 2, tipLength=0.3)
    
    # Rettangolo 2 (Bottom Left)
    cv2.rectangle(img, (50, 270), (420, 380), teal, 2)
    cv2.putText(img, "2. OPENCV & PUB (topic_foto)", (70, 305), cv2.FONT_HERSHEY_SIMPLEX, 0.6, white, 2)
    cv2.putText(img, "Legge la foto, converte in RGB", (70, 335), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    cv2.putText(img, "Invia i byte (Inizio Botta)", (70, 365), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    
    # Linea di collegamento complessa verso il blocco 3
    cv2.line(img, (420, 325), (660, 325), teal, 2)
    cv2.arrowedLine(img, (660, 325), (660, 200), teal, 2, tipLength=0.2)
    
    # Rettangolo 3 (Top Right)
    cv2.rectangle(img, (480, 120), (850, 200), teal, 2)
    cv2.putText(img, "3. SUBSCRIBER (topic_risposta)", (490, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.6, white, 2)
    cv2.putText(img, "Riceve il feedback da Nodo B", (490, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.5, gray, 1)
    
    cv2.imwrite('schema_timer.png', img)
    print("Immagine 'schema_timer.png' creata con successo!")

if __name__ == '__main__':
    crea_schema_trigger()
    crea_schema_timer()