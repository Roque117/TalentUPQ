import psycopg2
from psycopg2 import sql

def migrar_completo():
    # --- CONFIGURACIÓN CORREGIDA PARA TU NUEVA DB ---
    config = {
        "dbname": "BolsaTrabajoUPQ",
        "user": "postgres",
        "password": "TalentUPQ2026",
        "host": "dbtalento", # <--- Este es el nombre del servicio que creaste
        "port": "5432"
    }

    sql_script = """
    -- Limpieza
    DROP TABLE IF EXISTS Mensajes, Conversaciones, VacantesAprobadas, VacantesRevision, Notificaciones, Postulaciones, 
    VacanteHabilidadesOpcionales, VacanteHabilidadesRequeridas, Vacantes, CandidatoCompetencias, Competencias, 
    CandidatoHabilidades, Habilidades, Referencias, ExperienciaLaboral, PreparacionAcademica, Administradores, 
    Empresas, Candidatos, Usuarios CASCADE;

    CREATE TABLE Usuarios (
        UsuarioID SERIAL PRIMARY KEY,
        Email VARCHAR(100) UNIQUE NOT NULL,
        PasswordHash VARCHAR(255) NOT NULL,
        TipoUsuario VARCHAR(20) NOT NULL CHECK (TipoUsuario IN ('candidato', 'empresa', 'admin')),
        FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Activo BOOLEAN DEFAULT TRUE,
        ResetToken VARCHAR(100) NULL,
        ResetTokenExpira TIMESTAMP NULL
    );

    CREATE TABLE Candidatos (
        CandidatoID INT PRIMARY KEY,
        UsuarioID INT UNIQUE NOT NULL REFERENCES Usuarios(UsuarioID),
        Nombre VARCHAR(50) NOT NULL,
        ApellidoPaterno VARCHAR(50) NOT NULL,
        ApellidoMaterno VARCHAR(50),
        Telefono VARCHAR(20),
        EstadoCivil VARCHAR(20),
        Sexo VARCHAR(10),
        FechaNacimiento DATE,
        Nacionalidad VARCHAR(50),
        RFC VARCHAR(20),
        Direccion VARCHAR(200),
        Reubicacion BOOLEAN DEFAULT FALSE,
        Viajar BOOLEAN DEFAULT FALSE,
        LicenciaConducir BOOLEAN DEFAULT FALSE,
        ModalidadTrabajo VARCHAR(50),
        PuestoActual VARCHAR(100),
        PuestoSolicitado VARCHAR(100),
        FotoPerfil VARCHAR(255),
        CV VARCHAR(255),
        ResumenProfesional TEXT
    );

    CREATE TABLE Empresas (
        EmpresaID INT PRIMARY KEY,
        UsuarioID INT UNIQUE NOT NULL REFERENCES Usuarios(UsuarioID),
        Nombre VARCHAR(100) NOT NULL,
        Direccion VARCHAR(200),
        Telefono VARCHAR(20),
        SitioWeb VARCHAR(100),
        Descripcion TEXT,
        Logo VARCHAR(255),
        FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE Administradores (
        AdministradorID INT PRIMARY KEY,
        UsuarioID INT UNIQUE NOT NULL REFERENCES Usuarios(UsuarioID)
    );

    CREATE TABLE PreparacionAcademica (
        PreparacionID SERIAL PRIMARY KEY,
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        Grado VARCHAR(50) NOT NULL,
        Cedula VARCHAR(50),
        Estatus VARCHAR(20) NOT NULL,
        Institucion VARCHAR(100) NOT NULL,
        Pais VARCHAR(50) NOT NULL,
        FechaInicio DATE NOT NULL,
        FechaFin DATE
    );

    CREATE TABLE ExperienciaLaboral (
        ExperienciaID SERIAL PRIMARY KEY,
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        Empresa VARCHAR(100) NOT NULL,
        Domicilio VARCHAR(200),
        Telefono VARCHAR(20),
        Puesto VARCHAR(100) NOT NULL,
        FechaIngreso DATE NOT NULL,
        FechaSalida DATE,
        Funciones TEXT NOT NULL,
        SueldoInicial DECIMAL(10,2),
        SueldoFinal DECIMAL(10,2),
        MotivoSeparacion VARCHAR(200)
    );

    CREATE TABLE Referencias (
        ReferenciaID SERIAL PRIMARY KEY,
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        Nombre VARCHAR(100) NOT NULL,
        Ocupacion VARCHAR(100) NOT NULL,
        Telefono VARCHAR(20) NOT NULL,
        AnosConocer INT NOT NULL,
        Empresa VARCHAR(100),
        Documento VARCHAR(255)
    );

    CREATE TABLE Habilidades (
        HabilidadID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE CandidatoHabilidades (
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        HabilidadID INT NOT NULL REFERENCES Habilidades(HabilidadID),
        PRIMARY KEY (CandidatoID, HabilidadID)
    );

    CREATE TABLE Competencias (
        CompetenciaID SERIAL PRIMARY KEY,
        Nombre VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE CandidatoCompetencias (
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        CompetenciaID INT NOT NULL REFERENCES Competencias(CompetenciaID),
        PRIMARY KEY (CandidatoID, CompetenciaID)
    );

    CREATE TABLE Vacantes (
        VacanteID SERIAL PRIMARY KEY,
        EmpresaID INT NOT NULL REFERENCES Empresas(EmpresaID),
        Puesto VARCHAR(100) NOT NULL,
        GradoEstudios VARCHAR(50) NOT NULL,
        Resumen TEXT NOT NULL,
        Plazas INT NOT NULL DEFAULT 1,
        PlazasDisponibles INT NOT NULL DEFAULT 1,
        Estatus VARCHAR(20) NOT NULL CHECK (Estatus IN ('en_revision', 'aprobada', 'rechazada', 'cerrada')),
        FechaPublicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FechaAprobacion TIMESTAMP,
        ComentariosAdmin TEXT,
        Salario VARCHAR(100),
        TipoContrato VARCHAR(50) NOT NULL,
        Modalidad VARCHAR(20) NOT NULL,
        Ubicacion VARCHAR(200),
        ExperienciaRequerida VARCHAR(50) NOT NULL,
        Beneficios TEXT,
        FechaCierre DATE
    );

    CREATE TABLE VacanteHabilidadesRequeridas (
        VacanteID INT NOT NULL REFERENCES Vacantes(VacanteID),
        HabilidadID INT NOT NULL REFERENCES Habilidades(HabilidadID),
        PRIMARY KEY (VacanteID, HabilidadID)
    );

    CREATE TABLE VacanteHabilidadesOpcionales (
        VacanteID INT NOT NULL REFERENCES Vacantes(VacanteID),
        HabilidadID INT NOT NULL REFERENCES Habilidades(HabilidadID),
        PRIMARY KEY (VacanteID, HabilidadID)
    );

    CREATE TABLE Postulaciones (
        PostulacionID SERIAL PRIMARY KEY,
        VacanteID INT NOT NULL REFERENCES Vacantes(VacanteID),
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        FechaPostulacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Estatus VARCHAR(20) NOT NULL CHECK (Estatus IN ('pendiente', 'aceptado', 'rechazado')),
        Comentarios TEXT,
        CONSTRAINT UQ_Postulacion UNIQUE (VacanteID, CandidatoID)
    );

    CREATE TABLE Notificaciones (
        NotificacionID SERIAL PRIMARY KEY,
        EmpresaID INT NOT NULL REFERENCES Empresas(EmpresaID),
        Mensaje VARCHAR(255) NOT NULL,
        Tipo VARCHAR(20) NOT NULL,
        Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Leida BOOLEAN DEFAULT FALSE,
        VacanteID INT REFERENCES Vacantes(VacanteID),
        Comentarios TEXT
    );

    CREATE TABLE Conversaciones (
        ConversacionID SERIAL PRIMARY KEY,
        VacanteID INT NOT NULL REFERENCES Vacantes(VacanteID),
        CandidatoID INT NOT NULL REFERENCES Candidatos(CandidatoID),
        EmpresaID INT NOT NULL REFERENCES Empresas(EmpresaID),
        FechaInicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Activa BOOLEAN DEFAULT TRUE
    );

    CREATE TABLE Mensajes (
        MensajeID SERIAL PRIMARY KEY,
        ConversacionID INT NOT NULL REFERENCES Conversaciones(ConversacionID),
        RemitenteID INT NOT NULL,
        RemitenteTipo VARCHAR(20) NOT NULL,
        Mensaje TEXT NOT NULL,
        FechaEnvio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        Leido BOOLEAN DEFAULT FALSE,
        FechaLectura TIMESTAMP NULL
    );

    CREATE INDEX IX_Mensajes_Conversacion ON Mensajes(ConversacionID);
    CREATE INDEX IX_Mensajes_Leido ON Mensajes(Leido);
    CREATE INDEX IX_Conversaciones_Vacante ON Conversaciones(VacanteID);

    INSERT INTO Usuarios (Email, PasswordHash, TipoUsuario) VALUES 
    ('admin@upq.edu.mx', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin'),
    ('candidato@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'candidato'),
    ('empresa@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'empresa');

    INSERT INTO Administradores (AdministradorID, UsuarioID) VALUES (1, 1);
    INSERT INTO Candidatos (CandidatoID, UsuarioID, Nombre, ApellidoPaterno) VALUES (1, 2, 'Juan', 'Perez');
    INSERT INTO Empresas (EmpresaID, UsuarioID, Nombre) VALUES (1, 3, 'Empresa Ejemplo S.A.');
    
    INSERT INTO Habilidades (Nombre) VALUES 
    ('Python'), ('Java'), ('SQL'), ('JavaScript'), ('Flask'), ('Django'), ('HTML/CSS'), ('Git');
    """

    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        print("🚀 Conectado a la base de datos...")
        print("🏗️ Borrando y creando TODAS las tablas (18 tablas)...")
        cur.execute(sql_script)
        conn.commit()
        print("✅ ¡ÉXITO TOTAL! Tu base de datos está completa y lista.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    migrar_completo()