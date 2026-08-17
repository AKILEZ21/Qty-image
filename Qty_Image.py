import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider,QPushButton,QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PIL import Image
import io



# Valor de la Interfaz
ancho = 500
alto = 600
FORMATOS_VALIDO = (".jpg",".jpeg")
ESTILO_NORMAL = "border: 2px dashed gray;"
ESTILO_HOVER = "background-color: lightgray; border: 2px dashed gray;"


class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle("CALIDAD DE IMAGEN")
        self.label_tittle = QLabel("MODIFICA LA CALIDAD DE TU IMAGEN")
        self.label_tittle.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.resize(ancho,alto)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.label_tittle)
        self.label_tittle.setAlignment(Qt.AlignCenter)
        self.label_imagen = QLabel("Arrastra una imagen JPG aquí")
        self.label_imagen.setAlignment(Qt.AlignCenter)
        self.label_imagen.setMinimumHeight(400)
        self.label_imagen.setStyleSheet(ESTILO_NORMAL)
        self.layout.addWidget(self.label_imagen)
        self.slider_calidad = QSlider(Qt.Horizontal)
        self.slider_calidad.setRange(0,100)
        self.slider_calidad.setValue(100)
        self.layout.addWidget(self.slider_calidad)
        self.label_porcentaje = QLabel("Calidad: 100%")
        self.label_porcentaje.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_porcentaje)
        self.slider_calidad.valueChanged.connect(self.actualizar_calidad)
        self.boton_aceptar = QPushButton("Aceptar")
        self.layout.addWidget(self.boton_aceptar)
        self.boton_aceptar.clicked.connect(self.guardar_imagen)
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.setStyleSheet("background-color: red; color: white;")
        self.layout.addWidget(self.boton_cancelar)
        self.boton_cancelar.clicked.connect(self.close)

    def actualizar_calidad(self,valor):
        self.label_porcentaje.setText(f"Calidad: {valor}%")
        if hasattr(self, 'imagen_original'):
            self.mostrar_preview(valor)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.label_imagen.setStyleSheet(ESTILO_HOVER)
    def dragLeaveEvent(self, event):
        self.label_imagen.setStyleSheet(ESTILO_NORMAL)

    def mostrar_preview(self,calidad):
        buffer = io.BytesIO()
        self.imagen_original.save(buffer, format="JPEG", quality=calidad)
        buffer.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue())
        pixmap_escalado = pixmap.scaled(ancho, alto, Qt.KeepAspectRatio)
        self.label_imagen.setPixmap(pixmap_escalado)

    def dropEvent(self,event):
        self.label_imagen.setStyleSheet(ESTILO_NORMAL)
        urls = event.mimeData().urls()
        if urls:
            ruta_archivo = urls[0].toLocalFile()
            if ruta_archivo.lower().endswith(FORMATOS_VALIDO):
                self.ruta_actual = ruta_archivo
                self.imagen_original = Image.open(self.ruta_actual)
                self.mostrar_preview(self.slider_calidad.value())
            else:
                self.label_imagen.setText("Error, Formato no válido \n (Formatos Validos: .jpg, .jpeg)")

    def guardar_imagen(self):
        if not hasattr(self, "imagen_original"): return
        ruta_guardado, _= QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "JPEG Files (*.jpg *.jpeg)")
        if not ruta_guardado: return
        self.imagen_original.save(ruta_guardado, format="JPEG", quality=self.slider_calidad.value())
        

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())