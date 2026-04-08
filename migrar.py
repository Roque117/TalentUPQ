import psycopg2

def migrar():
    try:
        # Conexión (usa los mismos datos de tu hello.py)
        conn = psycopg2.connect(
            dbname="BolsaTrabajoUPQ",
            user="postgres",
            password="TalentUPQ2026",
            host="talent-upq-dbtalento-zkuf8m", # El host que funcionó en tu captura
            port="5432"
        )
        cur = conn.cursor()

        # Tu código SQL convertido a Postgres
        sql = """
        CREATE TABLE IF NOT EXISTS Usuarios (
            UsuarioID SERIAL PRIMARY KEY,
            Email VARCHAR(100) UNIQUE NOT NULL,
            PasswordHash VARCHAR(255) NOT NULL,
            TipoUsuario VARCHAR(20) NOT NULL CHECK (TipoUsuario IN ('candidato', 'empresa', 'admin')),
            FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS Candidatos (
            CandidatoID SERIAL PRIMARY KEY,
            UsuarioID INT UNIQUE NOT NULL REFERENCES Usuarios(UsuarioID),
            Nombre VARCHAR(50) NOT NULL,
            ApellidoPaterno VARCHAR(50) NOT NULL,
            Telefono VARCHAR(20)
        );

        CREATE TABLE IF NOT EXISTS Empresas (
            EmpresaID SERIAL PRIMARY KEY,
            UsuarioID INT UNIQUE NOT NULL REFERENCES Usuarios(UsuarioID),
            Nombre VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Vacantes (
            VacanteID SERIAL PRIMARY KEY,
            EmpresaID INT NOT NULL REFERENCES Empresas(EmpresaID),
            Puesto VARCHAR(100) NOT NULL,
            Estatus VARCHAR(20) DEFAULT 'en_revision'
        );
        """
        
        print("Creando tablas...")
        cur.execute(sql)
        conn.commit()
        print("¡Tablas creadas con éxito!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    migrar()