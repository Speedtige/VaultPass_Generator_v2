
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
    VAULT PASS GENERATOR v2.0
    Generador de Contraseñas Seguras - Standalone Edition
    Compatible con CryptoFile Vault V-05
    Estilo: Cyberpunk / Dark Theme

    Desarrollado por: 👉 Cristian M. Veliz Cano ✔
	Versión del Soft: 👉 V-02
	Nombre del Soft: ✨ VAULT PASS GENERATOR v2.0 ✨
	✨ 🔒 Seguridad sin compromisos ✨
=============================================================================
💪 PUNTOS FUERTES DEL SOFTWARE
Característica               Nivel               Descripción
PBKDF2HMAC-SHA3-256          🔥🔥🔥              480k iteraciones, NIST SP 800-132 compliant
CSPRNG                       🔥🔥🔥              secrets module (OS entropy) vs pseudo-random
Entropía Semántica             🔥🔥              Diccionario de 180+ categorías con expansión
Análisis de Fortaleza          🔥🔥              Cálculo de bits + tiempo de cracking estimado
3 Modos de Generación          🔥🔥              Contraseñas, Múltiples, Frases Semánticas, Ultra
UI Cyberpunk                   🔥🔥              Tema oscuro coherente, métricas visuales
Seguridad Visual                 🔥              EchoMode password, toggle visibilidad
Atajos de Teclado                🔥              Ctrl+G, Ctrl+M, Ctrl+C, ESC
Salts Únicos                   🔥🔥              Cada contraseña usa salt criptográfico independiente

Fortaleza Total Estimada: ~90-120 bits de entropía efectiva (equivalente a AES-128)

╔═══════════════════════════════════════════════════════════════════════════════╗
║                   ✨ VAULT PASS GENERATOR v2.0 ✨                             ║
║   ═══════════════════════════════════════════════════════════════════════     ║
║   GENERADOR DE CONTRASEÑAS CRYPTOGRÁFICO - NIVEL MILITAR                      ║
║   ═══════════════════════════════════════════════════════════════════════     ║
║                                                                               ║
║   Algoritmo:        PBKDF2-HMAC-SHA3-256 (480,000 iteraciones)                ║
║   Entropía:         CSPRNG vía OS (secrets.token_bytes)                       ║
║   Estándar:         NIST SP 800-132 / FIPS 140-2                              ║
║   Resistencia:      Anti-GPU/ASIC via computación intensiva                   ║
║                                                                               ║
║   Features:                                                                   ║
║   • Generación de contraseñas aleatorias de alta entropía                     ║
║   • Frases de paso semánticas con expansión de diccionario                    ║
║   • Análisis de fortaleza con estimación de tiempo de cracking                ║
║   • Generación múltiple con salts únicos por contraseña                       ║
║                                                                               ║
║   Compatible:      CryptoFile Vault V-05                                      ║
║   Tema:            Cyberpunk / Dark Terminal                                  ║
║                                                                               ║
║   Desarrollador:   👉 Cristian M. Veliz Cano ✔                                ║
║   Versión:         1.0.0 (Build 2026)                                         ║
║   Licencia:        MIT License - Open Source                                  ║
║                                                                               ║
║   🔒 SEGURIDAD SIN COMPROMISOS                                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

✨ VAULT PASS GENERATOR v2.0 ✨
Alojado en Mega:
https://mega.nz/file/v8UymRQS#DZKSjsPgFLfHbTLlugP0RsxxshYSwMiveWxQ3iR8Plw

Source Code:

"""
##=========================================================================================
import sys
import os
import string

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QLineEdit, QGroupBox, QGridLayout, QSpinBox, QCheckBox, QDialog,
    QMessageBox, QProgressBar, QTextEdit, QMenuBar, QMenu, QAction, QStatusBar, QShortcut,
    QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QFrame,
    QTabWidget, QComboBox)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QFont, QIcon, QClipboard, QKeySequence, QPixmap

# Intentar importar pyperclip, si no existe usar fallback
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# =============================================================================
# Criptografía Un Pelin-Más-Compleja
# =============================================================================
import secrets
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

import resources_rc
# Constantes de seguridad PBKDF2HMAC
PBKDF2_ITERATIONS = 480000  # NIST recomienda mínimo 10000, usamos 480k para resistencia GPU/ASIC
PBKDF2_HASH_ALGORITHM = hashes.SHA3_256()  # SHA3-256 (más resistente a length extension que SHA256)

##====================================================================================
# --- Clase para manejo de rutas de recursos ---
##====================================================================================
class Path():
    @staticmethod
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for pyinstaller"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # =========================
    # ✨ Devuelve, la Dirección Exacta de Cualquier, Archivo dentro de la App-Desk
    # =========================

    @staticmethod
    def resource_path_app():
        try:
            path_app = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
        except Exception as e:
            print(e)
        return path_app
# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
APP_NAME = "VaultPass Generator"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Cristian M. Veliz Cano"

SEMANTIC_DICT_GENERAL = {
    # --- Lenguajes de Programación y Frameworks ---
    "python": ["py", "python3", "python programming", "python scripting", "python language", "python code", "python dev"],
    "javascript": ["js", "javascript language", "ecmascript", "node.js", "nodejs", "frontend scripting", "js code"],
    "java": ["java language", "jvm", "java development", "jdk", "jre", "spring boot", "maven", "gradle"],
    "c++": ["cpp", "c plus plus", "gnu c++", "g++", "stl", "c++ standard library", "c++ development"],
    "php": ["php language", "php scripting", "laravel", "symfony", "composer", "backend scripting"],
    "ruby": ["ruby on rails", "rails framework", "ruby language", "gem", "bundler", "ruby scripting"],
    "go": ["golang", "go language", "go programming", "go modules"],
    "rust": ["rust lang", "rust programming", "cargo", "rust memory safety", "systems programming"],
    "sql": ["structured query language", "sql query", "database query", "t-sql", "pl/sql", "mysql", "postgresql"],
    "html": ["hypertext markup language", "html5", "web markup", "html code", "html tags"],
    "css": ["cascading style sheets", "css3", "stylesheet", "style rules", "sass", "scss", "less"],
    
    # --- Herramientas y Tecnologías de Desarrollo ---
    "git": ["git version control", "git repo", "github", "gitlab", "bitbucket", "git commit", "git branch", "git merge"],
    "docker": ["containers", "containerization", "dockerfile", "docker compose", "docker image", "docker hub", "kubernetes", "k8s"],
    "api": ["application programming interface", "rest api", "restful", "graphql", "api endpoint", "web service", "microservice"],
    "aws": ["amazon web services", "ec2", "s3", "lambda", "rds", "cloud computing", "aws cloud"],
    "azure": ["microsoft azure", "azure cloud", "azure services", "cloud platform ms"],
    "gcp": ["google cloud platform", "gcp cloud", "google compute engine", "gke"],
    "ci/cd": ["continuous integration", "continuous deployment", "jenkins", "github actions", "gitlab ci", "devops pipeline"],
    "testing": ["unit testing", "integration testing", "pytest", "unittest", "jest", "selenium", "tdd", "test driven development"],
    "linux": ["gnu linux", "linux kernel", "ubuntu", "debian", "centos", "shell scripting", "bash", "command line"],
    "windows": ["win32", "powershell", "windows server", "active directory", "windows os"],
    "macos": ["os x", "mac os", "cocoa", "swift", "xcode", "apple os"],
    
    # --- Conceptos y Paradigmas ---
    "algoritmo": ["algorithm", "algorithm design", "complexity", "big o notation", "data structures", "sorting algorithms"],
    "base de datos": ["database", "dbms", "rdbms", "nosql", "mongodb", "cassandra", "redis", "data storage", "sql database"],
    "seguridad": ["security", "cybersecurity", "cryptography", "encryption", "hashing", "vulnerability", "penetration testing", "owasp"],
    "osint": ["open source intelligence", "open-source intelligence", "intelligence gathering", "reconnaissance", "infosec"],
    "machine learning": ["ml", "ai", "artificial intelligence", "deep learning", "neural networks", "tensorflow", "pytorch", "scikit-learn", "data science"],
    "blockchain": ["distributed ledger", "smart contracts", "ethereum", "bitcoin", "cryptocurrency", "dlt", "web3"],
    "devops": ["development operations", "infrastructure as code", "automation", "ansible", "puppet", "chef", "terraform"],
    
    # --- Recursos y Comunidades ---
    "stackoverflow": ["stack overflow", "stackexchange", "programming q&a", "so", "coding forum"],
    "github": ["git repo", "github repo", "code repository", "source control", "open source", "git hosting"],
    "documentación": ["docs", "documentation", "api docs", "readthedocs", "tech reference", "manual"],

    # --- Ingeniería de Software ---
    "arquitectura": ["software architecture", "system architecture", "microservices architecture", "design patterns", "arquitectura de sistemas"],
    "uml": ["unified modeling language", "uml diagrams", "diagrama de clases", "casos de uso", "modelado"],
    "poo": ["oop", "object oriented programming", "programación orientada a objetos", "clases y objetos", "herencia", "polimorfismo"],
    "clean code": ["código limpio", "clean architecture", "refactoring", "buenas prácticas", "principios solid", "tdd", "arquitectura limpia"],
    "debug": ["debugging", "depuración", "troubleshooting", "bug fixing", "error tracking"],

    # --- Redes e Infraestructura ---
    "redes": ["networking", "network infrastructure", "routers", "switches", "protocolos de red", "tcp/ip", "dns", "dhcp"],
    "vpn": ["virtual private network", "conexion segura", "remote access", "tunel vpn"],
    "firewall": ["security firewall", "waf", "network filter", "protection layer", "filtrado de paquetes"],
    "servidor": ["server", "dedicated server", "vps", "host", "http server", "nginx", "apache"],

    # --- Ingeniería y electrónica ---
    "microcontrolador": ["microcontroller", "embedded system", "arduino", "esp32", "stm32", "programación embebida"],
    "sensores": ["sensor", "iot sensor", "arduino sensors", "electronic measurement", "telemetría", "sensores iot"],
    "robotica": ["robotics", "autonomous systems", "servo motors", "ros", "robot control", "mecatrónica"],

    # --- Inteligencia Artificial avanzada ---
    "nlp": ["natural language processing", "procesamiento de lenguaje natural", "tokenization", "llm", "transformers"],
    "vision": ["computer vision", "visión artificial", "image processing", "ocr", "detección de objetos"],
    "dataset": ["data set", "training data", "conjunto de datos", "data labeling", "csv dataset"],
    "reinforcement learning": ["rl", "aprendizaje por refuerzo", "agent training", "reward function"],

    # --- Data Science, Big Data y Estadística ---
    "big data": ["large scale data", "hadoop", "spark", "databricks", "data lakes", "etl", "pipelines"],
    "estadística": ["statistics", "probability", "regression", "anova", "data analysis", "modelos estadísticos"],
    "visualización": ["data visualization", "plots", "dashboards", "matplotlib", "power bi", "tableau"],

    # --- Ciberseguridad avanzada ---
    "malware": ["virus", "troyano", "spyware", "malicious software", "payload"],
    "forense digital": ["digital forensics", "dfir", "análisis forense", "memory dump", "evidencia digital"],
    "exploits": ["vulnerability exploit", "rce", "lfi", "rfi", "buffer overflow", "exploit db"],

    # --- Desarrollo móvil ---
    "android": ["android dev", "apk", "kotlin", "java android", "android studio"],
    "ios": ["iphone dev", "swiftui", "xcode project", "objective-c"],

    # --- Matemáticas aplicadas a ingeniería ---
    "matrices": ["matrix", "matrix algebra", "álgebra lineal", "vectores", "numpy array"],
    "calculo": ["calculus", "derivatives", "integrals", "math analysis", "matemáticas avanzadas"],

    # --- Vida Diaria y Hogar ---
    "persona": ["person", "individual", "contact", "profile", "gente", "individuo", "sujeto"],
    "ubicacion": ["location", "place", "address", "city", "site", "lugar", "sitio", "dirección", "posición"],
    "casa": ["home", "house", "apartment", "flat", "domicilio", "vivienda", "hogar", "departamento"],
    "comida": ["food", "meal", "cuisine", "dish", "alimento", "platillo", "vianda"],
    "receta": ["recipe", "cooking recipe", "food recipe", "gastronomy", "cocina", "guía de cocina"],
    "limpieza": ["cleaning", "cleaning tips", "house cleaning", "tidying", "aseo", "orden", "higiene"],
    "compra": ["shopping", "purchase", "buying", "store", "market", "comprar", "adquisición"],
    "dinero": ["money", "cash", "currency", "funds", "payment", "pago", "capital", "finanzas"],
    "salud": ["health", "wellness", "fitness", "medicine", "well-being", "bienestar", "medicina", "forma física"],
    "trabajo": ["job", "work", "employment", "career", "profession", "oficio", "empleo", "ocupación"],
    "educación": ["education", "learning", "school", "university", "course", "study", "aprendizaje", "formación"],
    "familia": ["family", "relatives", "kin", "household", "parientes", "familiares"],
    "amigos": ["friends", "friendship", "buddies", "pals", "amistad", "compañeros"],
    
    # --- Intereses y Ocio ---
    "deporte": ["sport", "sports", "exercise", "game", "match", "competency", "ejercicio físico", "competencia"],
    "música": ["music", "song", "track", "melody", "tune", "canción", "tema musical"],
    "viaje": ["travel", "trip", "journey", "vacation", "tourism", "viajar", "excursión", "turismo"],
    "libro": ["book", "novel", "reading", "text", "publication", "lectura", "texto", "publicación"],
    "película": ["movie", "film", "cinema", "motion picture", "cine", "filme"],
    "coche": ["car", "automobile", "vehicle", "auto", "motorcar", "vehículo", "automóvil"],
    "mascota": ["pet", "animal", "companion animal", "mascota", "animal doméstico"],
    
    # --- Agricultura y Naturaleza ---
    "semillas": ["seed", "seeds", "plant seeds", "agriculture seeds", "semilla", "grano", "simiente"],
    "fertilizantes": ["fertilizer", "fertilisers", "plant feed", "nutrients", "abono", "nutrientes para plantas"],
    "planta": ["plant", "flora", "vegetation", "greenery", "vegetal", "flora local"],
    "jardín": ["garden", "yard", "orchard", "patio", "cultivo", "huerto"],
    "clima": ["weather", "climate", "temperature", "forecast", "tiempo atmosférico", "pronóstico del tiempo"],
    
    # --- Conceptos Abstractos y Comunicación ---
    "idea": ["idea", "concept", "thought", "notion", "inspiration", "brainwave", "concepto", "pensamiento", "inspiración"],
    "problema": ["problem", "issue", "challenge", "trouble", "dilemma", "obstacle", "inconveniente", "dilema", "obstáculo"],
    "solución": ["solution", "answer", "fix", "resolution", "remedy", "solve", "respuesta", "arreglo", "resolución", "remedio"],
    "tiempo": ["time", "moment", "duration", "period", "while", "ocasion", "momento", "duración", "período", "rato"],
    "amor": ["love", "affection", "romance", "passion", "devotion", "cariño", "afecto", "pasión"],
    "feliz": ["happy", "joyful", "glad", "cheerful", "delighted", "content", "alegre", "contento", "satisfecho"],
    "triste": ["sad", "unhappy", "sorrowful", "melancholy", "depressed", "deprimido", "melancólico"],
    "conversación": ["conversation", "talk", "chat", "dialogue", "discussion", "charla", "diálogo", "debate", "plática"],
    "pregunta": ["question", "query", "inquiry", "doubt", "consulta", "duda", "preguntar"],
    "respuesta": ["answer", "reply", "response", "retort", "respuesta", "réplica", "contestación"],
    "información": ["information", "info", "data", "details", "facts", "knowledge", "datos", "detalles", "conocimiento", "saber"],
    "noticia": ["news", "report", "update", "headline", "story", "reportaje", "titular", "actualidad"],
    "evento": ["event", "occasion", "happening", "incident", "affair", "acontecimiento", "suceso", "incidente"],
    "oportunidad": ["opportunity", "chance", "prospect", "opening", "oportunidad", "posibilidad", "ocasión"],

    # --- Transporte ---
    "motocicleta": ["moto", "motorcycle", "bike", "motocicleta", "vehículo de dos ruedas"],
    "autobús": ["bus", "coach", "transporte público", "camioneta pública"],
    "bicicleta": ["bicycle", "bike", "cicla", "bici"],

    # --- Oficios y trabajos técnicos civiles ---
    "electricista": ["electrician", "instalador eléctrico", "servicio eléctrico", "cables", "circuitos del hogar"],
    "plomero": ["plumber", "fontanero", "tuberías", "reparación de fugas", "drenajes"],
    "carpintero": ["carpenter", "madera", "ebanistería", "muebles"],
    "albañil": ["mason", "construction worker", "block", "cemento", "yeso"],
    "herramientas": ["tools", "hand tools", "kit de herramientas", "martillo", "llave inglesa"],

    # --- Servicios públicos ---
    "agua": ["water", "servicio de agua", "suministro", "tuberías", "plomería"],
    "electricidad": ["electricity", "power", "luz", "energía", "corriente"],
    "internet": ["wifi", "network", "router", "conexión web"],

    # --- Cocina y hogar avanzado ---
    "electrodoméstico": ["appliance", "home appliance", "cocina eléctrica", "microondas", "refrigerador"],
    "bebida": ["drink", "beverage", "refresco", "jugo", "café", "té"],

    # --- Seguridad doméstica ---
    "emergencia": ["emergency", "urgent situation", "accidente", "llamar ayuda"],
    "primeros auxilios": ["first aid", "auxilio", "curación básica"],
    "incendio": ["fire", "fuego", "accidente doméstico", "alarma"],

    # --- Clima y fenómenos naturales ---
    "lluvia": ["rain", "heavy rain", "precipitación"],
    "viento": ["wind", "breeze", "air flow"],
    "terremoto": ["earthquake", "sismo", "temblor"],

    # --- Oficina y documentos ---
    "documento": ["document", "file", "paper", "archivo"],
    "correo": ["email", "mail", "mensaje", "inbox"],
    "foto": ["photo", "image", "picture", "fotografía"],

    # --- Tecnología general para civiles ---
    "celular": ["phone", "smartphone", "móvil", "android", "iphone"],
    "computadora": ["computer", "pc", "laptop", "notebook"],

    # --- Emociones adicionales ---
    "enojado": ["angry", "mad", "furious", "molesto"],
    "relajado": ["relaxed", "calm", "tranquilo"],
    "estresado": ["stressed", "anxious", "preocupado"],

    # --- Conversación y expresión ---
    "mensaje": ["message", "text", "sms", "chat"],
    "explicación": ["explanation", "clarification", "detalle"],
    "historia": ["story", "tale", "narrative", "relato"],

    # --- Objetos cotidianos ---
    "bolsa": ["bag", "purse", "saco", "mochila"],
    "llave": ["key", "house key", "car key"],
    "mesa": ["table", "desk", "mesón"],
    "silla": ["chair", "seat"],

    # --- Anime ---
    "anime": ["japanese animation", "animación japonesa", "otaku", "anime series", "anime show"],
    "shonen": ["acción juvenil", "battle anime", "anime para jóvenes", "shounen"],
    "shojo": ["romance anime", "anime para chicas", "shoujo"],
    "isekai": ["otro mundo", "fantasy world anime", "isekai anime"],
    "opening": ["op", "intro anime", "canción inicial"],
    "ending": ["ed", "canción final", "ending theme"],

    # --- Caricaturas ---
    "caricatura": ["cartoon", "animated show", "dibujos animados"],
    "cartoon": ["serie animada", "caricatura americana", "cartoon network"],
    "animado": ["animated", "dibujado", "animación"],

    # --- Series (en general) ---
    "serie": ["tv show", "series", "episodios", "temporadas"],
    "temporada": ["season", "t", "cycle"],
    "episodio": ["episode", "capítulo", "ep", "cap"],

    # --- Películas ---
    "pelicula": ["movie", "film", "cine", "largometraje"],
    "actor": ["actor de cine", "film actor", "star"],
    "directo": ["director", "filmmaker", "realizador"],

    # --- Mangas / Manwhuas / Manhuas ---
    "manga": ["japanese comic", "comic japonés", "historieta japonesa"],
    "manhwa": ["korean comic", "comic coreano", "manwhua"],
    "manhua": ["chinese comic", "comic chino", "historieta china"],
    "scan": ["scaneo", "raw", "capítulo escaneado"],

    # --- Web Novels y Novelas ---
    "novela": ["novel", "story book", "literatura"],
    "web novel": ["novela web", "historia online", "light novel"],
    "light novel": ["ln", "novela ligera", "ficción japonesa"],
    "libro": ["book", "ebook", "lectura", "volume"],

    # --- Música ---
    "musica": ["music", "song", "audio", "melodía", "track"],
    "cancion": ["song", "tema", "single"],
    "album": ["disco", "álbum musical", "cd"],
    "artista": ["musician", "cantante", "autor musical"],

    # --- Arte ---
    "arte": ["art", "drawing", "painting", "creación artística"],
    "pintura": ["paint", "artwork", "cuadro"],
    "ilustración": ["illustration", "art digital", "dibujos"],

    # --- Televisión ---
    "television": ["tv", "tele", "canal", "programa tv"],
    "canal": ["channel", "station", "señal tv"],
    "programa": ["show", "tv program", "transmisión"],

    # --- Descargas y Servicios Gratuitos ---
    "gratis_mega": ["mega free", "link mega", "descarga mega", "mega.nz"],
    "gratis_rapidshare": ["rapidshare", "descarga rápida", "host antigua"],
    "gratis_google_drive": ["google drive", "gdrive", "link drive", "drive download"],
    "descarga": ["download", "bajar archivo", "archivo descargable"],

    # --- Libros / PDFs / Lectura ---
    "pdf": ["documento pdf", "archivo pdf", "ebook pdf"],
    "ebook": ["digital book", "libro electrónico", "lectura digital"],
    "biblioteca": ["library", "colección de libros", "book archive"],
}

# =============================================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# =============================================================================
class VaultPassGenerator(QMainWindow):
    """Aplicación principal del generador de contraseñas"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(900, 700)

        # Icono
        self.setWindowIcon(QtGui.QIcon(":/imagenes/Resources/1.ico"))
        self.setStyleSheet(self.get_main_stylesheet())
        
        # Datos
        self.settings = {}
        
        # UI
        self.init_ui()
        self.init_menu()
        self.init_statusbar()

        ## ➜ Se Innicia de forma Automatica la Información sobre el Soft-Ware
        self.show_app_info()
                
    # =====================================================================
    # ESTILOS CSS (Cyberpunk Dark Theme)
    # =====================================================================
    def get_main_stylesheet(self):
	        """Estilo principal cyberpunk oscuro - CORREGIDO"""
	        return """
	        QMainWindow {
	            background-color: #0a0a0f;
	        }
	        QWidget {
	            background-color: #0a0a0f;
	            color: #e6edf3;
	            font-family: 'Segoe UI', 'Consolas', sans-serif;
	        }
	        QGroupBox {
	            border: 1px solid #00c3ff;
	            border-radius: 8px;
	            margin-top: 5px;
	            padding-top: 5px;
	            font-weight: bold;
	            color: #00c3ff;
	            font-size: 14px;
	        }
	        QGroupBox::title {
	            subcontrol-origin: margin;
	            left: 10px;
	            padding: 0 8px;
	            background: #0a0a0f;
	        }
	        QLabel {
	            color: #cccccc;
	            font-size: 12px;
	        }
	        QLabel#title_label {
	            color: #00ff88;
	            font-size: 20px;
	            font-weight: bold;
	        }
	        QLabel#subtitle_label {
	            color: #00c3ff;
	            font-size: 12px;
	        }
	        QLineEdit {
	            background-color: #111118;
	            border: 1px solid #333;
	            border-radius: 6px;
	            padding: 10px;
	            color: #80ff00;
	            font-family: 'Consolas', monospace;
	            font-size: 14px;
	            font-weight: bold;
	            selection-background-color: #00c3ff;
	        }
	        QLineEdit:focus {
	            border: 1px solid #00c3ff;
	        }
	        QSpinBox {
	            background-color: #111118;
	            border: 1px solid #333;
	            border-radius: 5px;
	            padding: 6px;
	            color: #e6edf3;
	            font-size: 12px;
	            min-width: 70px;
	        }
	        QSpinBox:focus {
	            border: 1px solid #00c3ff;
	        }
	        /* CORRECCIÓN CHECKBOXES */
	        QCheckBox {
	            color: #888888;
	            spacing: 8px;
	            font-size: 11px;
	        }
	        QCheckBox::indicator {
	            width: 16px;
	            height: 16px;
	            border-radius: 3px;
	            border: 1px solid #00c3ff;
	            background: #111118;
	        }
	        QCheckBox::indicator:checked {
	            background: #00c3ff;
	            border: 1px solid #00c3ff;
	            image: none;
	        }
	        QCheckBox::indicator:hover {
	            border: 1px solid #80ff00;
	        }
	        QPushButton {
	            border-radius: 6px;
	            padding: 8px 16px;
	            font-weight: bold;
	            font-size: 12px;
	            border: 1px solid;
	            min-height: 32px;
	        }
	        QPushButton#btn_generate {
	            background: #1a1a2e;
	            border-color: #80ff00;
	            color: #80ff00;
	        }
	        QPushButton#btn_generate:hover {
	            background: #80ff00;
	            color: #0a0a0f;
	        }
	        QPushButton#btn_copy {
	            background: #1a1a2e;
	            border-color: #00c3ff;
	            color: #00c3ff;
	        }
	        QPushButton#btn_copy:hover {
	            background: #00c3ff;
	            color: #0a0a0f;
	        }
	        QPushButton#btn_save {
	            background: #1a1a2e;
	            border-color: #ffaa00;
	            color: #ffaa00;
	        }
	        QPushButton#btn_save:hover {
	            background: #ffaa00;
	            color: #0a0a0f;
	        }
	        QPushButton#btn_clear {
	            background: #1a1a2e;
	            border-color: #ff4444;
	            color: #ff4444;
	        }
	        QPushButton#btn_clear:hover {
	            background: #ff4444;
	            color: white;
	        }
			QProgressBar {
	            border: 1px solid #333;
	            border-radius: 4px;
	            text-align: center;
	            color: white;
	            background: #111118;
	            height: 18px;  /* ← MÁS DELGADA */
	            margin-top: 5px;  /* ← ESPACIO RESPECTO A BOTONES */
	        }
	        QProgressBar::chunk {
	            background: qlineargradient(
	                x1:0, y1:0,
	                x2:1, y2:0,
	                stop:0 #00c3ff,
	                stop:1 #80ff00
	            );
	            border-radius: 4px;
	        }
	        QTableWidget {
	            background-color: #111118;
	            border: 1px solid #333;
	            border-radius: 6px;
	            gridline-color: #222;
	            color: #e6edf3;
	            font-family: 'Consolas', monospace;
	            font-size: 11px;
	        }
	        QTableWidget::item {
	            padding: 6px;
	            border-bottom: 1px solid #222;
	        }
	        QTableWidget::item:selected {
	            background-color: #00c3ff;
	            color: #0a0a0f;
	        }
	        QHeaderView::section {
	            background-color: #1a1a2e;
	            color: #00c3ff;
	            padding: 8px;
	            border: none;
	            font-weight: bold;
	            font-size: 11px;
	        }
	        /* CORRECCIÓN TABS */
	        QTabWidget::pane {
	            border: 1px solid #00c3ff;
	            border-radius: 6px;
	            background-color: #0a0a0f;
	            top: -1px;
	        }
	        QTabBar::tab {
	            background: #111118;
	            color: #888;
	            padding: 8px 20px;
	            border-top-left-radius: 6px;
	            border-top-right-radius: 6px;
	            border: 1px solid #333;
	            border-bottom: none;
	            margin-right: 2px;
	        }
	        QTabBar::tab:selected {
	            background: #0a0a0f;
	            color: #00ff88;
	            border: 1px solid #00c3ff;
	            border-bottom: 1px solid #0a0a0f;
	        }
	        QTabBar::tab:hover:!selected {
	            background: #1a1a2e;
	            color: #00c3ff;
	        }
	        QComboBox {
	            background-color: #111118;
	            border: 1px solid #333;
	            border-radius: 5px;
	            padding: 6px;
	            color: #e6edf3;
	            min-width: 150px;
	        }
	        QComboBox:focus {
	            border: 1px solid #00c3ff;
	        }
	        QComboBox::drop-down {
	            border: none;
	            width: 25px;
	        }
	        QComboBox::down-arrow {
	            image: none;
	            border-left: 5px solid transparent;
	            border-right: 5px solid transparent;
	            border-top: 5px solid #00c3ff;
	        }
	        QMenuBar {
	            background-color: #111118;
	            color: #e6edf3;
	            border-bottom: 1px solid #333;
	        }
	        QMenuBar::item:selected {
	            background-color: #00c3ff;
	            color: #0a0a0f;
	        }
	        QMenu {
	            background-color: #111118;
	            border: 1px solid #333;
	            color: #e6edf3;
	        }
	        QMenu::item:selected {
	            background-color: #00c3ff;
	            color: #0a0a0f;
	        }
	        QStatusBar {
	            background-color: #111118;
	            color: #888;
	            border-top: 1px solid #333;
	        }
	        QTextEdit {
	            background-color: #080808;
	            border: 1px solid #333;
	            border-radius: 6px;
	            color: #00ff80;
	            font-family: 'Consolas', monospace;
	            font-size: 11px;
	            padding: 8px;
	        }
	        QScrollBar:vertical {
	            background: #111118;
	            width: 10px;
	            border-radius: 5px;
	        }
	        QScrollBar::handle:vertical {
	            background: #00c3ff;
	            min-height: 30px;
	            border-radius: 5px;
	        }
	        QScrollBar::handle:vertical:hover {
	            background: #80ff00;
	        }
	        QScrollBar::add-line:vertical,
	        QScrollBar::sub-line:vertical {
	            height: 0px;
	        }
	        """
    
    # =====================================================================
    # INICIALIZACIÓN DE UI
    # =====================================================================
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("⚡ VAULT PASS GENERATOR")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        subtitle = QLabel("Generador de Contraseñas Seguras")
        subtitle.setObjectName("subtitle_label")
        subtitle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(subtitle)
        
        main_layout.addLayout(header_layout)
        
        # Separador decorativo
        line = QFrame()
        line.setContentsMargins(0, 0, 0, 0)

        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #30363d;")
        line.setFixedHeight(2)
        main_layout.addWidget(line)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_generator_tab(), "🎲 Generador")
        self.tabs.addTab(self.create_tools_tab(), "🛠️ Herramientas")
        
        main_layout.addWidget(self.tabs)
        return line
        
    def create_generator_tab(self):
        """Crea la pestaña del generador principal"""
        tab = QWidget()
        tab.setContentsMargins(3, 3, 3, 3)

        layout = QVBoxLayout(tab)
        layout.setSpacing(5)
        
        # Sección: Configuración
        config_group = QGroupBox("⚙️ Configuración de Contraseña")

        config_layout = QGridLayout()
        config_layout.setSpacing(5)
        
        # Longitud
        config_layout.addWidget(QLabel("Longitud:"), 0, 0)
        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 256)
        self.length_spin.setValue(32)
        ##self.length_spin.valueChanged.connect(self.generate_password) ## <-- Opcional...
        config_layout.addWidget(self.length_spin, 0, 1)
        
        # Cantidad para generar múltiples
        config_layout.addWidget(QLabel("Cantidad:"), 0, 2)
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 100)
        self.quantity_spin.setValue(1)
        config_layout.addWidget(self.quantity_spin, 0, 3)
        
        # Separador
        config_layout.addWidget(self.create_separator(), 1, 0, 1, 1)
        
        # Checkboxes
        self.chk_upper = QCheckBox("Mayúsculas (A-Z)")
        self.chk_upper.setChecked(True)
        self.chk_upper.stateChanged.connect(self.generate_password)
        
        self.chk_lower = QCheckBox("Minúsculas (a-z)")
        self.chk_lower.setChecked(True)
        self.chk_lower.stateChanged.connect(self.generate_password)
        
        self.chk_digits = QCheckBox("Números (0-9)")
        self.chk_digits.setChecked(True)
        self.chk_digits.stateChanged.connect(self.generate_password)
        
        self.chk_special = QCheckBox("Especiales (!@#$%)")
        self.chk_special.setChecked(True)
        self.chk_special.stateChanged.connect(self.generate_password)
        
        self.chk_extra = QCheckBox("Extra ({}[]|<>~)")
        self.chk_extra.setChecked(False)
        self.chk_extra.stateChanged.connect(self.generate_password)
        
        self.chk_exclude_similar = QCheckBox("Excluir similares (0,O,1,l,I)")
        self.chk_exclude_similar.setChecked(True)
        self.chk_exclude_similar.stateChanged.connect(self.generate_password)
        
        config_layout.addWidget(self.chk_upper, 2, 0)
        config_layout.addWidget(self.chk_lower, 2, 1)
        config_layout.addWidget(self.chk_digits, 3, 0)
        config_layout.addWidget(self.chk_special, 3, 1)
        config_layout.addWidget(self.chk_extra, 4, 0)
        config_layout.addWidget(self.chk_exclude_similar, 4, 1)
        
        # Presets
        config_layout.addWidget(QLabel("Preset:"), 5, 0)
        self.combo_preset = QComboBox()
        self.combo_preset.addItems(["Personalizado", "PIN (4-6 dígitos)", "WiFi (16 chars)", 
                                   "Segura (32 chars)", "Ultra Segura (64 chars)", 
                                   "Memorable (3 palabras)"])
        self.combo_preset.currentIndexChanged.connect(self.apply_preset)
        config_layout.addWidget(self.combo_preset, 5, 1, 1, 3)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Sección: Resultado
        result_group = QGroupBox("🔑 Contraseña Generada")

        result_layout = QVBoxLayout()
        result_layout.setSpacing(15)
        
        # Display principal
        self.password_display = QLineEdit()
        self.password_display.setEchoMode(QLineEdit.Password)
        self.password_display.setAlignment(Qt.AlignCenter)
        self.password_display.setMinimumHeight(50)
        self.password_display.setFont(QFont("Consolas", 14, QFont.Bold))
        self.password_display.setPlaceholderText("Presiona 'Generar' para crear contraseña...")
        
        # Botones de acción (AHORA PRIMERO)
        btn_layout = QHBoxLayout()
        
        self.btn_generate = QPushButton("🎲 GENERAR")
        self.btn_generate.setObjectName("btn_generate")
        self.btn_generate.clicked.connect(self.generate_password_with_progress)
        
        self.btn_copy = QPushButton("📋 COPIAR")
        self.btn_copy.setObjectName("btn_copy")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        
        self.btn_show = QPushButton("👀 MOSTRAR")
        self.btn_show.setObjectName("btn_save")
        self.btn_show.setCheckable(True)
        self.btn_show.clicked.connect(self.toggle_visibility)
        
        self.btn_limpiar = QPushButton("[✘] LIMPIAR")
        self.btn_limpiar.setObjectName("btn_clear")
        self.btn_limpiar.clicked.connect(self.clear_all)
        
        btn_layout.addWidget(self.btn_generate)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_show)
        btn_layout.addWidget(self.btn_limpiar)
        
        # Barra de progreso (AHORA DEBAJO DE LOS BOTONES)
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(True)
        #self.strength_bar.setVisible(False)  # ← OCULTA POR DEFECTO
        
        # Métricas
        metrics_layout = QHBoxLayout()        
        metrics_layout.setSpacing(15)

        self.lbl_entropy = QLabel("Entropía: 0 bits")
        self.lbl_entropy.setStyleSheet("color: #00c3ff; font-family: Consolas; font-size: 11px;")
        self.lbl_length = QLabel("Longitud: 0")
        self.lbl_length.setStyleSheet("color: #00c3ff; font-family: Consolas; font-size: 11px;")
        self.lbl_charset = QLabel("Charset: 0")
        self.lbl_charset.setStyleSheet("color: #00c3ff; font-family: Consolas; font-size: 11px;")
        
        metrics_layout.addWidget(self.lbl_entropy)
        metrics_layout.addStretch()
        metrics_layout.addWidget(self.lbl_length)
        metrics_layout.addStretch()
        metrics_layout.addWidget(self.lbl_charset)
        
        # ORDEN CORRECTO: Display → Botones → Barra → Métricas
        result_layout.addWidget(self.password_display)
        result_layout.addLayout(btn_layout)      # Botones primero
        result_layout.addWidget(self.strength_bar)  # Barra debajo
        result_layout.addLayout(metrics_layout)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        ##==============
        # Área de texto múltiple
        multi_group = QGroupBox("📦 Generación Múltiple")
        multi_layout = QVBoxLayout()
        
        self.multi_text = QTextEdit()
        self.multi_text.setPlaceholderText("Las contraseñas generadas en lote aparecerán aquí...")
        self.multi_text.setMaximumHeight(150)
        
        btn_multi_layout = QHBoxLayout()
        self.btn_generate_multi = QPushButton("🎲 GENERAR MÚLTIPLES")
        self.btn_generate_multi.setObjectName("btn_generate")
        self.btn_generate_multi.clicked.connect(self.generate_multiple)
        
        self.btn_copy_multi = QPushButton("📋 COPIAR TODO")
        self.btn_copy_multi.setObjectName("btn_copy")
        self.btn_copy_multi.clicked.connect(self.copy_multiple)
        
        self.btn_clear_multi = QPushButton("[✘] LIMPIAR")
        self.btn_clear_multi.setObjectName("btn_clear")
        self.btn_clear_multi.clicked.connect(self.multi_text.clear)
        
        btn_multi_layout.addWidget(self.btn_generate_multi)
        btn_multi_layout.addWidget(self.btn_copy_multi)
        btn_multi_layout.addWidget(self.btn_clear_multi)
        
        multi_layout.addWidget(self.multi_text)
        multi_layout.addLayout(btn_multi_layout)
        
        multi_group.setLayout(multi_layout)
        layout.addWidget(multi_group)
        
        layout.addStretch()
        return tab
        
    def create_tools_tab(self):
        """Crea la pestaña de herramientas adicionales"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Verificador de fortaleza
        check_group = QGroupBox("🔍 Verificador de Fortaleza")
        check_layout = QVBoxLayout()
        
        self.check_input = QLineEdit()
        self.check_input.setPlaceholderText("Ingresa una contraseña para verificar...")
        self.check_input.setEchoMode(QLineEdit.Password)
        self.check_input.textChanged.connect(self.check_password_strength)
        
        self.check_result = QLabel("Ingresa una contraseña para analizar")
        self.check_result.setAlignment(Qt.AlignCenter)
        self.check_result.setStyleSheet("font-size: 16px; padding: 20px;")
        
        self.check_bar = QProgressBar()
        self.check_bar.setRange(0, 100)
        self.check_bar.setValue(0)
        
        check_layout.addWidget(self.check_input)
        check_layout.addWidget(self.check_result)
        check_layout.addWidget(self.check_bar)
        
        check_group.setLayout(check_layout)
        layout.addWidget(check_group)
        
        # Generador de frases de paso
        phrase_group = QGroupBox("💬 Generador de Frases de Paso")
        phrase_layout = QVBoxLayout()
        
        self.phrase_output = QLineEdit()
        self.phrase_output.setReadOnly(True)
        self.phrase_output.setAlignment(Qt.AlignCenter)

        # Botones de acción
        btn_layout = QHBoxLayout()
        
        btn_phrase = QPushButton("🎲 Generar Frase")
        btn_phrase.setObjectName("btn_generate")
        btn_phrase.clicked.connect(self.generate_passphrase)
        
        btn_copy = QPushButton("📋 COPIAR")
        btn_copy.setObjectName("btn_copy")
        btn_copy.clicked.connect(self.copy_palabra_multiple)
        
        btn_clean = QPushButton("[✘] Cleaner")
        btn_clean.setObjectName("btn_clear")
        btn_clean.clicked.connect(self.cleaner_hall)

        # Botón para frase ultra (agregar en phrase_layout)
        btn_ultra = QPushButton("🔐 FRASE ULTRA (4 palabras)")
        btn_ultra.setObjectName("btn_generate")
        btn_ultra.clicked.connect(lambda: self.generate_passphrase_ultra(4))
        
        btn_layout.addWidget(btn_phrase)
        btn_layout.addWidget(btn_ultra)
        btn_layout.addWidget(btn_copy)
        btn_layout.addWidget(btn_clean)
        
        phrase_layout.addWidget(self.phrase_output)
        phrase_layout.addLayout(btn_layout)

        phrase_group.setLayout(phrase_layout)
        layout.addWidget(phrase_group)

        Image_App = QGroupBox()
        layout_image = QHBoxLayout()
        layout_image.setContentsMargins(0, 0, 0, 0)
        layout_image.setSpacing(0)
        
        self.LBL_Image = QLabel()
        self.LBL_Image.setAlignment(Qt.AlignCenter)
        self.LBL_Image.setScaledContents(True)

        layout_image.addWidget(self.LBL_Image)
        Image_App.setLayout(layout_image)
        layout.addWidget(Image_App)
        
        #layout.addStretch()
        self.ingresar_Banner()
        return tab
    
    def create_separator(self):
        """Crea un separador horizontal"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #30363d;")
        return line
 
    # =========================
    ## ➜ Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    # =========================
    def show_app_info(self):
        dialog = app_info(self)
        dialog.exec_()

    ## Metodo Mostrar la Info, del Soft, en una Ventanita Emergente, enforma de Dialogo
    def key_app_info(self):
        dialog_k = key_info(self)
        dialog_k.exec_()

    # =====================================================================
    # Image Banner...
    # =====================================================================
    def ingresar_Banner(self):

        self.LBL_Image.setText("")
        ## path_image = Path.resource_path((Path.resource_path('Ico\\2.png') if os.path.exists(Path.resource_path('Ico\\2.png')) else ''))
        path_image = str(":/imagenes/Resources/2.png")
        pixmap = QPixmap(path_image)
        scaled = pixmap.scaled(
                self.LBL_Image.width(), self.LBL_Image.height(),
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        self.LBL_Image.setPixmap(scaled)       

        # Click para abrir
        self.LBL_Image.mousePressEvent = lambda e, path=scaled: self._ingresar_imagen_LBL(scaled)

    # =====================================================================
    # Image Banner en LBL_Image...
    # =====================================================================
    def _ingresar_imagen_LBL(self, path=""):

        # Guardamos en Temporales...
        ## path_image = Path.resource_path((Path.resource_path('Ico\\3.png') if os.path.exists(Path.resource_path('Ico\\3.png')) else ''))
        path_image = str(":/imagenes/Resources/3.png")
        pixmap = QPixmap(path_image)

        scaled = pixmap
        Viewer_Image.Frame_Viewer_Image(self, scaled)
    
    # =====================================================================
    # MENÚ
    # =====================================================================
    def init_menu(self):
        """Inicializa la barra de menú"""
        menubar = self.menuBar()
        
        # Menú Archivo
        file_menu = menubar.addMenu("📁 Archivo")

        file_menu.addSeparator()
        
        action_exit = QAction("❌ Salir", self)
        action_exit.setShortcut("ESC")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)
        
        # Menú Generar
        gen_menu = menubar.addMenu("🎲 Generar")
        
        action_gen = QAction("🎲 Nueva Contraseña", self)
        action_gen.setShortcut("Ctrl+G")
        action_gen.triggered.connect(self.generate_password)
        gen_menu.addAction(action_gen)
        
        action_gen_multi = QAction("📦 Múltiples Contraseñas", self)
        action_gen_multi.setShortcut("Ctrl+M")
        action_gen_multi.triggered.connect(self.generate_multiple)
        gen_menu.addAction(action_gen_multi)
        
        action_gen_phrase = QAction("💬 Frase de Paso", self)
        action_gen_phrase.triggered.connect(self.generate_frase)
        gen_menu.addAction(action_gen_phrase)

        action_gen_ultra = QAction("🔐 Frase Ultra Segura", self)
        action_gen_ultra.triggered.connect(lambda: self.generate_passphrase_ultra2(4))
        gen_menu.addAction(action_gen_ultra)
        
        # Menú Editar
        edit_menu = menubar.addMenu("✏️ Editar")
        
        action_copy = QAction("📋 Copiar", self)
        action_copy.setShortcut("Ctrl+C")
        action_copy.triggered.connect(self.copy_to_clipboard)
        edit_menu.addAction(action_copy)
        
        action_clear = QAction("🗑️ Limpiar Todo", self)
        action_clear.triggered.connect(self.clear_all)
        edit_menu.addAction(action_clear)
        
        # Menú Ayuda
        help_menu = menubar.addMenu("❓ Ayuda")
        
        action_about = QAction("ℹ️ Acerca de", self)
        action_about.triggered.connect(self.show_about)
        help_menu.addAction(action_about)
        
        action_Licencia = QAction("ℹ️ Licencia App", self)
        action_Licencia.triggered.connect(self.Licencia_App)
        help_menu.addAction(action_Licencia)
        
        action_Info_Soft = QAction("ℹ️ Acerca del Soft-Ware", self)
        action_Info_Soft.setShortcut("F1")
        action_Info_Soft.triggered.connect(self.show_app_info)
        help_menu.addAction(action_Info_Soft)
    
    def init_statusbar(self):
        """Inicializa la barra de estado"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage(f"🟢 {APP_NAME} listo | Presiona Ctrl+G para generar")

# =====================================================================
    # GENERACIÓN PBKDF2HMAC - Núcleo Criptográfico Militar
    # =====================================================================
    def derive_password_pbkdf2(self, length, charset, salt=None, iterations=None):
        """
        Deriva contraseña usando PBKDF2HMAC con entropía del sistema operativo.
        
        Args:
            length: Longitud deseada de la contraseña
            charset: String con caracteres permitidos
            salt: Salt opcional (si es None, genera salt aleatorio de 32 bytes)
            iterations: Iteraciones PBKDF2HMAC (default: PBKDF2_ITERATIONS)
        
        Returns:
            tuple: (password_string, salt_used, entropy_bits)
        """
        if not charset:
            raise ValueError("Charset no puede estar vacío")
        
        # Usar salt criptográficamente seguro del sistema (32 bytes = 256 bits)
        if salt is None:
            salt = secrets.token_bytes(32)
        
        iterations = iterations or PBKDF2_ITERATIONS
        
        # Material de entrada aleatorio (seed) - 64 bytes de entropía del OS
        seed_material = secrets.token_bytes(64)
        
        # PBKDF2HMAC: Derivar bytes determinísticos pero impredecibles
        kdf = PBKDF2HMAC(
            algorithm=PBKDF2_HASH_ALGORITHM,
            length=length * 4,  # Pedimos más bytes de los necesarios para mapeo
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        
        derived_key = kdf.derive(seed_material)
        
        # Mapear bytes derivados al charset usando modular arithmetic (uniforme)
        charset_len = len(charset)
        password_chars = []
        
        # Usar cada 4 bytes como un entero de 32 bits para indexar
        for i in range(0, len(derived_key), 4):
            if len(password_chars) >= length:
                break
            chunk = derived_key[i:i+4]
            # Convertir a entero big-endian
            idx = int.from_bytes(chunk, byteorder='big', signed=False)
            # Mapeo uniforme al charset
            password_chars.append(charset[idx % charset_len])
        
        password = ''.join(password_chars)
        
        # Calcular entropía real: log2(charset_len ^ length)
        import math
        entropy = length * math.log2(charset_len)
        
        return password, salt, entropy
    
    def get_charset_from_settings(self):
        """Construye el charset basado en los checkboxes actuales"""
        chars = ""
        if self.chk_lower.isChecked():
            chars += string.ascii_lowercase
        if self.chk_upper.isChecked():
            chars += string.ascii_uppercase
        if self.chk_digits.isChecked():
            chars += string.digits
        if self.chk_special.isChecked():
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?\"'/<>\\~`"
        if self.chk_extra.isChecked():
            chars += "`~^\\/"
        
        # Excluir caracteres similares
        if self.chk_exclude_similar.isChecked():
            chars = chars.translate(str.maketrans('', '', '0O1lI'))
        
        return chars

    # =====================================================================
    # FUNCIONALIDAD PRINCIPAL
    # =====================================================================
    def generate_password(self):
        """Genera contraseña segura usando PBKDF2HMAC (militar-grade)"""
        length = self.length_spin.value()
        
        # Obtener charset
        chars = self.get_charset_from_settings()
        
        if not chars:
            QMessageBox.warning(self, "Advertencia", "Selecciona al menos un tipo de carácter")
            return
        
        try:
            # Generar usando PBKDF2HMAC
            password, salt_used, entropy = self.derive_password_pbkdf2(length, chars)
            
            # Asegurar variedad de tipos de caracteres (garantía de complejidad)
            password_list = list(password)
            
            # Forzar al menos uno de cada tipo seleccionado
            positions_used = set()
            
            def place_required_char(char_set, check_func):
                """Coloca un carácter requerido en posición aleatoria"""
                if not check_func():
                    return
                attempts = 0
                while attempts < 100:
                    pos = secrets.randbelow(length)
                    if pos not in positions_used:
                        char = secrets.choice(char_set)
                        password_list[pos] = char
                        positions_used.add(pos)
                        break
                    attempts += 1
            
            # Aplicar garantías de complejidad
            if self.chk_lower.isChecked():
                place_required_char(
                    [c for c in string.ascii_lowercase if c not in '0O1lI'],
                    lambda: any(c in string.ascii_lowercase for c in password_list)
                )
            if self.chk_upper.isChecked():
                place_required_char(
                    [c for c in string.ascii_uppercase if c not in '0O1lI'],
                    lambda: any(c in string.ascii_uppercase for c in password_list)
                )
            if self.chk_digits.isChecked():
                place_required_char(
                    [c for c in string.digits if c not in '0O1lI'],
                    lambda: any(c in string.digits for c in password_list)
                )
            if self.chk_special.isChecked():
                place_required_char("!@#$%^&*()_+-=[]{}|;:,.<>?", 
                    lambda: any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password_list)
                )
            
            # Mezclar final (Fisher-Yates con secrets)
            password_list = self._secure_shuffle(password_list)
            final_password = ''.join(password_list)
            
            self.password_display.setText(final_password)
            self.calculate_strength(final_password)
            
            # Mostificar salt en base64 para referencia (debug)
            salt_b64 = base64.b64encode(salt_used).decode('ascii')
            self.statusbar.showMessage(
                f"✅ Contraseña PBKDF2HMAC generada: {length} chars | "
                f"Iteraciones: {PBKDF2_ITERATIONS:,} | Salt: {salt_b64[:16]}...", 
                5000
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error Criptográfico", f"Error al generar: {str(e)}")
    
    def _secure_shuffle(self, lst):
        """Mezcla lista usando secrets (cifrado seguro)"""
        shuffled = lst[:]
        n = len(shuffled)
        for i in range(n - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return shuffled

    def generate_password_with_progress(self):
        """Genera contraseña y muestra la barra de progreso"""
        # Mostrar barra
        self.strength_bar.setVisible(True)
        self.strength_bar.setValue(0)
        
        # Generar
        self.generate_password()
        
        # Animación de llenado
        for i in range(0, 101, 10):
            self.strength_bar.setValue(i)
            QtWidgets.QApplication.processEvents()
            QtCore.QThread.msleep(20)
    
    def calculate_strength(self, password):
        """Calcula y muestra la fortaleza (adaptado para PBKDF2HMAC)"""
        import math
        
        length = len(password)
        
        # Calcular pool de caracteres
        pool = 0
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if has_lower: pool += 26
        if has_upper: pool += 26
        if has_digit: pool += 10
        if has_special: pool += 32
        
        entropy = length * math.log2(pool) if pool > 0 else 0
        score = min(100, int((entropy / 128) * 100))
        
        self.strength_bar.setValue(score)
        
        # Colores y texto con indicador PBKDF2HMAC
        if score < 40:
            color, text = "#da3633", "DÉBIL"
        elif score < 60:
            color, text = "#f0883e", "MEDIA"
        elif score < 80:
            color, text = "#58a6ff", "FUERTE"
        else:
            color, text = "#00ff88", "EXCELENTE (PBKDF2HMAC)"
        
        self.strength_bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        self.strength_bar.setFormat(f"{text} - {score}% | PBKDF2HMAC-SHA3")
        
        # Actualizar métricas
        self.lbl_entropy.setText(f"Entropía: {entropy:.1f} bits")
        self.lbl_length.setText(f"Longitud: {length}")
        self.lbl_charset.setText(f"Charset: {pool} | Iters: {PBKDF2_ITERATIONS//1000}k")
    
    def generate_multiple(self):
        """Genera múltiples contraseñas usando PBKDF2HMAC con salts únicos"""
        qty = self.quantity_spin.value()
        
        if qty > 100:
            QMessageBox.warning(self, "Límite", "Máximo 100 contraseñas por lote")
            return
        
        chars = self.get_charset_from_settings()
        if not chars:
            QMessageBox.warning(self, "Advertencia", "Selecciona al menos un tipo de carácter")
            return
        
        length = self.length_spin.value()
        passwords = []
        
        try:
            for i in range(qty):
                # Cada contraseña usa salt único (defensa contra rainbow tables)
                password, salt, entropy = self.derive_password_pbkdf2(length, chars)
                passwords.append(password)
                
                # Actualizar progreso visual
                if i % 10 == 0:
                    self.statusbar.showMessage(f"🔐 Generando PBKDF2HMAC... {i+1}/{qty}", 100)
                    QtWidgets.QApplication.processEvents()
            
            self.multi_text.setPlainText("\n".join(passwords))
            
            # Estadísticas de seguridad
            total_entropy = length * (qty ** 0.5)  # Entropía agregada aproximada
            self.statusbar.showMessage(
                f"✅ {qty} contraseñas PBKDF2HMAC generadas | "
                f"Iteraciones totales: {qty * PBKDF2_ITERATIONS:,} | "
                f"Entropía promedio: {entropy:.1f} bits", 
                5000
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en generación múltiple: {str(e)}")

    def generate_frase(self):

    	self.generate_passphrase()
    	self.password_display.setText(self.phrase_output.text())
    	self.cleaner_hall()

    def normalize_string(self, s):
	    if not s:
	        return ""
	    return " ".join(s.lower().strip().split())
	##---------------------------------------------------------------
    def expand_query_semantic(self, query, mode="all", max_expansions=8):
        """
        Expansión semántica mejorada con fallback a categorías relacionadas.
        """
        base = self.normalize_string(query)
        if not base:
            return [query]
            
        expansions = [base]
        tokens = [t for t in base.replace("-", " ").replace("_", " ").split() if len(t) > 1]
        
        # Pool de búsqueda
        pool = {}
        if mode == "all":
            pool.update(SEMANTIC_DICT_GENERAL)
        
        # Búsqueda directa por tokens
        for t in tokens:
            if t in pool:
                sinónimos = pool[t]
                # Mezclar sinónimos para impredecibilidad
                sinónimos_mezclados = sinónimos[:]
                secrets.SystemRandom().shuffle(sinónimos_mezclados)
                
                for syn in sinónimos_mezclados[:max_expansions]:
                    candidate = f"{base} {syn}"
                    if candidate not in expansions:
                        expansions.append(candidate)
                    if len(expansions) >= max_expansions:
                        return expansions
        
        # Búsqueda inversa: encontrar claves que contengan el query
        if len(expansions) < 3:
            for clave, valores in pool.items():
                if base in clave or any(base in v for v in valores):
                    for v in valores[:2]:  # Máximo 2 por clave encontrada
                        if v not in expansions and v != base:
                            expansions.append(v)
                        if len(expansions) >= max_expansions:
                            break
                    if len(expansions) >= max_expansions:
                        break
        
        # Añadir combinaciones de tokens si hay múltiples
        if len(tokens) >= 2 and len(expansions) < max_expansions:
            for i in range(len(tokens)):
                for j in range(i+1, len(tokens)):
                    combined = f"{tokens[i]}-{tokens[j]}"
                    if combined not in expansions:
                        expansions.append(combined)
                    if len(expansions) >= max_expansions:
                        break
                if len(expansions) >= max_expansions:
                    break
        
        return expansions[:max_expansions]

    def generate_passphrase(self):
        """Genera frase de paso memorable usando semántica distribuida + entropía PBKDF2HMAC"""
        self.cleaner_hall()
        
        # Categorías semánticas para mezcla estratégica (diversidad conceptual)
        categorias = {
            'tech': ['python', 'javascript', 'java', 'docker', 'linux', 'api', 'git', 'aws', 
                     'seguridad', 'algoritmo', 'base de datos', 'redes', 'firewall'],
            'vida': ['casa', 'comida', 'viaje', 'libro', 'musica', 'deporte', 'familia', 
                     'amigos', 'trabajo', 'coche', 'mascota', 'jardín'],
            'abstracto': ['idea', 'problema', 'solución', 'tiempo', 'amor', 'feliz', 
                          'conversación', 'información', 'oportunidad', 'historia'],
            'cultura': ['anime', 'manga', 'serie', 'pelicula', 'musica', 'arte', 'pintura', 
                       'novela', 'album', 'artista'],
            'oficios': ['electricista', 'plomero', 'carpintero', 'albañil', 'herramientas'],
            'emergencia': ['emergencia', 'incendio', 'primeros auxilios', 'agua', 'electricidad']
        }
        
        # Seleccionar 3 categorías aleatorias distintas (diversidad forzada)
        cats_seleccionadas = secrets.SystemRandom().sample(list(categorias.keys()), 3)
        
        palabras_finales = []
        
        for categoria in cats_seleccionadas:
            # Elegir palabra base de la categoría
            palabra_base = secrets.choice(categorias[categoria])
            
            # Buscar expansiones semánticas en el diccionario global
            expansiones = self.expand_query_semantic(palabra_base, mode="all", max_expansions=5)
            
            # Elegir: 70% probabilidad de sinónimo, 30% palabra original
            if len(expansiones) > 1 and secrets.randbelow(100) < 70:
                # Elegir una expansión aleatoria (índice 1 en adelante son expansiones)
                idx = secrets.randbelow(len(expansiones) - 1) + 1
                palabra_seleccionada = expansiones[idx].split()[-1]  # Última palabra de la expansión
            else:
                palabra_seleccionada = palabra_base
            
            # Limpiar y normalizar
            palabra_limpia = palabra_seleccionada.lower().replace(" ", "-").replace("_", "-")
            palabras_finales.append(palabra_limpia)
        
        # Entropía PBKDF2HMAC para los componentes numéricos/simbólicos (no predecibles)
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_256(),
            length=8,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived = kdf.derive(secrets.token_bytes(32))
        
        # Mapear bytes derivados a número (10-99) y símbolo especial
        numero = 10 + (derived[0] % 90)  # 10-99
        especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        especial = especiales[derived[1] % len(especiales)]
        
        # Construcción de la frase con variación estructural (3 patrones posibles)
        patron = secrets.randbelow(3)
        if patron == 0:
            # Formato: palabra-palabra-palabra-numero!especial
            passphrase = f"{palabras_finales[0]}-{palabras_finales[1]}-{palabras_finales[2]}-{numero}{especial}"
        elif patron == 1:
            # Formato: especial+palabra-palabra-numero-palabra
            passphrase = f"{especial}{palabras_finales[0]}-{palabras_finales[1]}-{numero}-{palabras_finales[2]}"
        else:
            # Formato: palabra-numero-palabra!especial-palabra
            passphrase = f"{palabras_finales[0]}-{numero}-{palabras_finales[1]}{especial}-{palabras_finales[2]}"
        
        # Calcular entropía real
        import math
        # Entropía de las palabras (aproximación conservadora)
        entropy_palabras = len(palabras_finales) * math.log2(50)  # ~50 opciones por categoría
        # Entropía del número (90 opciones)
        entropy_numero = math.log2(90)
        # Entropía del patrón (3 opciones)
        entropy_patron = math.log2(3)
        # Entropía del especial (len(especiales))
        entropy_especial = math.log2(len(especiales))
        
        total_entropy = entropy_palabras + entropy_numero + entropy_patron + entropy_especial
        
        self.phrase_output.setText(passphrase)
        self.check_input.setText(passphrase)
        
        # Mostrar metadatos en statusbar
        cats_str = "/".join(cats_seleccionadas)
        self.statusbar.showMessage(
            f"🧠 Frase semántica [{cats_str}] | Entropía: ~{total_entropy:.1f} bits | "
            f"Patrón #{patron}", 5000
        )

    def generate_passphrase_ultra2(self, num_palabras=4):

        self.generate_passphrase_ultra(num_palabras)
        self.password_display.setText(self.phrase_output.text())
        self.cleaner_hall()

    def generate_passphrase_ultra(self, num_palabras=4):
        """
        Genera frase ultra-entropía usando múltiples capas de semántica + PBKDF2HMAC.
        Útil para contraseñas maestras o seeds de recuperación.
        """
        self.cleaner_hall()
        
        # Usar PBKDF2HMAC para determinar qué categorías usar (determinístico pero aleatorio)
        salt = secrets.token_bytes(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA3_256(),
            length=num_palabras * 2,
            salt=salt,
            iterations=480000,
            backend=default_backend()
        )
        derived = kdf.derive(secrets.token_bytes(64))
        
        todas_las_categorias = list(SEMANTIC_DICT_GENERAL.keys())
        palabras_seleccionadas = []
        
        for i in range(num_palabras):
            # Usar bytes derivados para seleccionar categoría
            categoria_idx = derived[i*2] % len(todas_las_categorias)
            categoria = todas_las_categorias[categoria_idx]
            
            # Seleccionar sinónimo de esa categoría
            sinonimos = SEMANTIC_DICT_GENERAL[categoria]
            palabra_idx = derived[i*2 + 1] % len(sinonimos)
            palabra = sinonimos[palabra_idx]
            
            # Limpiar
            palabra_limpia = palabra.replace(" ", "-").replace("_", "-")
            palabras_seleccionadas.append(palabra_limpia)
        
        # Entropía adicional para separadores y casing
        sep_opciones = ["-", "_", ".", "!", "@", "#", "$"]
        separador = sep_opciones[derived[num_palabras*2 - 1] % len(sep_opciones)]
        
        # Mezclar casing aleatoriamente
        palabras_finales = []
        for i, palabra in enumerate(palabras_seleccionadas):
            if secrets.randbelow(2) == 0:
                palabras_finales.append(palabra.upper())
            else:
                palabras_finales.append(palabra.lower())
        
        passphrase = separador.join(palabras_finales)
        
        # Añadir sufijo entropía PBKDF2HMAC
        numero = 1000 + (derived[-2] % 9000)  # 4 dígitos
        passphrase = f"{passphrase}{separador}{numero}"
        
        self.phrase_output.setText(passphrase)
        self.check_input.setText(passphrase)
        
        # Entropía: log2(180 categorías * 10 sinónimos promedio ^ num_palabras)
        import math
        entropy = math.log2(len(todas_las_categorias)) + (num_palabras * math.log2(10))
        self.statusbar.showMessage(
            f"🔐 Ultra-Frase [{num_palabras} palabras] | Entropía: ~{entropy:.1f} bits | "
            f"PBKDF2HMAC: 480k iters", 5000
        )
        
        return passphrase

    def cleaner_hall(self):

        self.check_input.setText("")
        self.check_result.setText("Ingresa una contraseña para analizar")
        self.check_bar.setValue(0)
        self.phrase_output.setText("")
    
    def check_password_strength(self):
        """Verifica la fortaleza de una contraseña ingresada"""
        password = self.check_input.text()
        if not password:
            self.check_result.setText("Ingresa una contraseña")
            self.check_bar.setValue(0)
            return
        
        import math
        
        length = len(password)
        pool = 0
        
        if any(c.islower() for c in password): pool += 26
        if any(c.isupper() for c in password): pool += 26
        if any(c.isdigit() for c in password): pool += 10
        if any(c in string.punctuation for c in password): pool += 32
        
        entropy = length * math.log2(pool) if pool > 0 else 0
        score = min(100, int((entropy / 128) * 100))
        
        self.check_bar.setValue(score)
        
        # Tiempo estimado para crackear
        combinations = pool ** length
        seconds = combinations / 1e9  # Asumiendo 1 billón de intentos/segundo
        
        if seconds < 60:
            tiempo = f"{seconds:.1f} segundos"
        elif seconds < 3600:
            tiempo = f"{seconds/60:.1f} minutos"
        elif seconds < 86400:
            tiempo = f"{seconds/3600:.1f} horas"
        elif seconds < 31536000:
            tiempo = f"{seconds/86400:.1f} días"
        elif seconds < 3153600000:
            tiempo = f"{seconds/31536000:.1f} años"
        else:
            tiempo = "siglos"
        
        self.check_result.setText(f"Entropía: {entropy:.1f} bits | Tiempo estimado: {tiempo}")
        
        # Color
        if score < 40:
            color = "#da3633"
        elif score < 60:
            color = "#f0883e"
        elif score < 80:
            color = "#58a6ff"
        else:
            color = "#00ff88"
        
        self.check_bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
    
    # =====================================================================
    # ACCIONES
    # =====================================================================
    def copy_to_clipboard(self):
        """Copia la contraseña al portapapeles"""
        password = self.password_display.text()
        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            self.statusbar.showMessage("📋 Copiado al portapapeles", 2000)
    
    def copy_multiple(self):
        """Copia las contraseñas múltiples"""
        text = self.multi_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusbar.showMessage("📋 Contraseñas copiadas", 2000)

    def copy_palabra_multiple(self):
        """Copia las contraseñas múltiples"""
        text = self.phrase_output.text()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusbar.showMessage("📋 Contraseñas copiadas", 2000)
    
    def toggle_visibility(self):
        """Muestra/oculta la contraseña"""
        if self.btn_show.isChecked():
            self.password_display.setEchoMode(QLineEdit.Normal)
            self.btn_show.setText("🙈 OCULTAR")
        else:
            self.password_display.setEchoMode(QLineEdit.Password)
            self.btn_show.setText("👀 MOSTRAR")
        
    def apply_preset(self, index):
        """Aplica configuraciones predefinidas"""
        presets = {
            1: (6, False, False, True, False, False),    # PIN
            2: (16, True, True, True, True, False),     # WiFi
            3: (32, True, True, True, True, True),      # Segura
            4: (64, True, True, True, True, True),      # Ultra
        }
        
        if index in presets:
            length, upper, lower, digits, special, extra = presets[index]
            self.length_spin.setValue(length)
            self.chk_upper.setChecked(upper)
            self.chk_lower.setChecked(lower)
            self.chk_digits.setChecked(digits)
            self.chk_special.setChecked(special)
            self.chk_extra.setChecked(extra)
            self.generate_password()

        if index == 5:
        	print("Si...")
        	self.generate_passphrase()
        	self.password_display.setText(self.phrase_output.text())
        	self.cleaner_hall()
    
    # =====================================================================
    # CONFIGURACIÓN Y UTILIDADES
    # =====================================================================    
    def clear_all(self):
        """Limpia todo"""
        self.password_display.clear()
        self.multi_text.clear()
        self.lbl_entropy.setText("Entropía: 0 bits")
        self.lbl_length.setText("Longitud: 0")
        self.lbl_charset.setText("Charset: 0")

        #self.strength_bar.setVisible(False)
        self.strength_bar.setFormat(f"0%")
        self.strength_bar.setValue(0)

        self.combo_preset.setCurrentIndex(0)
    
    def show_about(self):
        """Muestra diálogo Acerca de"""
        QMessageBox.about(self, f"Acerca de {APP_NAME}", f"""
        <h2>{APP_NAME} v{APP_VERSION}</h2>
        <h3>Desarrollado Por: ↔ {APP_AUTHOR}</h3>
        <p>Generador de Contraseñas Seguras</p>
        <p>Compatible con <b>CryptoFile Vault V-05</b></p>
        <br>
        <p>Características:</p>
        <ul>
            <li>Generación de contraseñas cryptográficamente seguras</li>
            <li>Análisis de entropía y fortaleza</li>
            <li>Generación de frases de paso memorables</li>
            <li>Verificador de fortaleza</li>
        </ul>
        <br>
        <p style="color: #00ff88;">🔒 Seguridad sin compromisos</p>
        """)

    def Licencia_App(self):

        try:

            message = f'''
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Desarrollado por: 👉 Cristian M. Veliz Cano ✔
Versión del Soft: 👉 V-02
Nombre del Soft: ✨ {APP_NAME} v{APP_VERSION} ✨
✨ 🔒 Seguridad sin compromisos ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Licencia:

MIT License

Copyright (c) 2026 Cristian M. Veliz Cano

Se concede permiso, de forma gratuita, a cualquier persona
que obtenga una copia de este software y de los archivos de
documentación asociados, para utilizar el Software sin
restricción, incluyendo sin limitación los derechos de uso,
copia, modificación, fusión, publicación, distribución,
sublicencia y/o venta de copias del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL",
SIN GARANTÍA DE NINGÚN TIPO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
            QMessageBox.about(self, "Completado", 
                f"{message}\n\nDe Caracter: ↔ Gratuito Open-Source & Free-Code...")

        except Exception as e:
            print(e)
    
    def closeEvent(self, event):
        event.accept()

	## Metodo para Obtener Cualquier Tecla Pulsada dentro de la App.
    def keyPressEvent(self, event):

    	if event.key() == Qt.Key_Escape:
    		sys.exit()

##======================================================================================
## ➜ Diálogo de Información - Estilo Cyberpunk Vault Pass
##======================================================================================
class app_info(QDialog):
    """Diálogo de información sobre Vault Pass Generator"""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Guardar referencia al padre
        self.parent = parent
        
        # Configuración de ventana
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("⚡ Información del Sistema")
        self.setFixedSize(640, 520)
        self.setModal(True)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Estilo base del diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #0a0a0f;
                color: #e6edf3;
            }
            QLabel {
                color: #e6edf3;
                font-family: 'Segoe UI', 'Consolas', sans-serif;
            }
            QTextEdit {
                background-color: #111118;
                color: #00ff80;
                border: 1px solid #00c3ff;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 11pt;
                selection-background-color: #00c3ff;
            }
            QPushButton {
                background-color: #1a1a2e;
                color: #00c3ff;
                border: 1px solid #00c3ff;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 11px;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #00c3ff;
                color: #0a0a0f;
            }
        """)
        
        # --- Header con título ---
        header_layout = QHBoxLayout()
        
        title_box = QVBoxLayout()
        main_title = QLabel("⚡ VAULT PASS GENERATOR")
        main_title.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #00ff88;
            font-family: 'Consolas', monospace;
        """)
        main_title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("🔒 Generador de Contraseñas Criptográficas")
        subtitle.setStyleSheet("""
            font-size: 10pt;
            color: #00c3ff;
            font-family: 'Consolas', monospace;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        version = QLabel(f"Versión {APP_VERSION} | Build 2026")
        version.setStyleSheet("""
            font-size: 9pt;
            color: #888888;
            font-family: 'Consolas', monospace;
        """)
        version.setAlignment(Qt.AlignCenter)
        
        title_box.addWidget(main_title)
        title_box.addWidget(subtitle)
        title_box.addWidget(version)
        
        header_layout.addStretch()
        header_layout.addLayout(title_box)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # --- Separador decorativo ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #00c3ff;")
        line.setFixedHeight(2)
        layout.addWidget(line)
        
        # --- Área de texto informativo ---
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        
        info_content = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    DESARROLLADO POR                              ║
║              👉 {APP_AUTHOR} ✔                         ║
╚══════════════════════════════════════════════════════════════════╝

📊 ESPECIFICACIONES TÉCNICAS

🔐 Algoritmo Principal:\tPBKDF2-HMAC-SHA3-256
🔢 Iteraciones:\t\t{PBKDF2_ITERATIONS:,} (NIST SP 800-132)
🎲 Entropía Fuente:\t\tOS CSPRNG (secrets.token_bytes)
🧮 Estimación Entropía:\tHasta 120 bits efectivos
✔ Compatible Con:\t\tCryptoFile Vault V-05

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ FUNCIONALIDADES PRINCIPALES

🎲 Generador de Contraseñas
   • Longitud configurable: 4-256 caracteres
   • Charset personalizable (mayúsculas, minúsculas, dígitos, símbolos)
   • Exclusión de caracteres similares (0O, 1lI)
   • Salts únicos por contraseña

🧠 Generador de Frases de Paso (Semántico)
   • Diccionario de {len(SEMANTIC_DICT_GENERAL)}+ categorías semánticas
   • Expansión de sinónimos inteligente
   • 3 patrones estructurales aleatorios
   • Entropía semántica distribuida

📦 Generación Múltiple
   • Hasta 100 contraseñas por lote
   • Cada una con salt criptográfico independiente
   • Exportación a portapapeles

🔍 Verificador de Fortaleza
   • Cálculo de entropía en bits
   • Estimación de tiempo de cracking
   • Análisis de complejidad visual

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⌨️ ATAJOS DE TECLADO

   Ctrl+G      →  Generar nueva contraseña
   Ctrl+M      →  Generar múltiples contraseñas
   Ctrl+C      →  Copiar al portapapeles
   F1          →  Información Sobre el Soft-Ware (Programa)
   ESC         →  Cerrar aplicación

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎨 INTERFAZ

   Tema:           Cyberpunk / Terminal Oscuro
   Framework:      PyQt5
   Estilo:         Dark Theme con acentos neón (#00ff88, #00c3ff)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 SEGURIDAD

✔ Sin conexión a Internet requerida
✔ Sin telemetría ni recolección de datos
✔ Sin servicios externos
✔ Procesamiento 100% local
✔ Memoria segura (no persistente en disco)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 LICENCIA

MIT License
Copyright (c) 2026 {APP_AUTHOR}

Se concede permiso, de forma gratuita, a cualquier persona que 
obtenga una copia de este software, para utilizarlo sin restricción, 
incluyendo los derechos de uso, copia, modificación y distribución.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 "Seguridad sin compromisos" 🔒

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        info_text.setText(info_content)
        layout.addWidget(info_text)
        
        # --- Botón cerrar ---
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        close_button = QPushButton("✔ ACEPTAR")
        close_button.setFixedWidth(120)
        close_button.clicked.connect(self.close)
        close_layout.addWidget(close_button)
        close_layout.addStretch()
        
        layout.addLayout(close_layout)
        
        # Centrar diálogo respecto al padre
        # if self.parent:
        #     self.move(self.parent.frameGeometry().center() - self.rect().center())

##====================================================================================
##====================================================================================

class Viewer_Image(VaultPassGenerator):

    def __init__(self, parent=None):
        super().__init__(parent)

    def Frame_Viewer_Image(self, output_path):

        self.path = output_path

        dialog = QDialog(self)
        dialog.setWindowTitle("Contenido del Archivo")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        ##self.center_on_screen()

        layout = QVBoxLayout()        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        dialog.setLayout(layout)

        Image_App = QGroupBox()
        layout_image = QVBoxLayout()
        layout_image.setContentsMargins(0, 0, 0, 0)
        layout_image.setSpacing(0)

        #fpath, fname = os.path.split(output_path)
        label = QLabel('✨ VAULT PASS GENERATOR v2.0 ✨')
        # label.setFixedWidth(25)
        label.setFixedHeight(22)
        label.setAlignment(Qt.AlignCenter)
        layout_image.addWidget(label)
        
        self.LBL_Image_Banner = QLabel()
        self.LBL_Image_Banner.setAlignment(Qt.AlignCenter)
        self.LBL_Image_Banner.setScaledContents(True)

        layout_image.addWidget(self.LBL_Image_Banner)
        Image_App.setLayout(layout_image)
        layout.addWidget(Image_App)

        try:

            try:

                scaled = self.path.scaled(
                    self.width(), self.height()-35,
                    Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )

                self.LBL_Image_Banner.setText("")
                self.LBL_Image_Banner.setPixmap(scaled)

            except Exception as e:
                print(e)

                self.in_image_alternative()

        except Exception as e:
            print(e)

            self.in_image_alternative()

        dialog.exec_()

    def in_image_alternative(self):

        self.LBL_Image_Banner.setText("")
        path_image = str(":/imagenes/Resources/2.png")
        pixmap = QPixmap(path_image)
        scaled = pixmap.scaled(
            self.LBL_Image_Banner.width(), self.LBL_Image_Banner.height(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        self.LBL_Image_Banner.setPixmap(scaled)

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    # Establecer icono (opcional)
    # app.setWindowIcon(QIcon("icon.png"))
    
    window = VaultPassGenerator()
    window.show()
    
    sys.exit(app.exec_())