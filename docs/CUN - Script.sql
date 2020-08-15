--Tables
-- Table: tbl_administradores_transf
CREATE TABLE tbl_administradores_transf (
    admin_id varchar2(20)  NOT NULL,
    admin_nombres varchar2(255)  NOT NULL,
    admin_apellidos varchar2(255)  NOT NULL,
    admin_email varchar2(50)  NOT NULL,
    admin_telefono varchar2(50)  NOT NULL,
    admin_cargo varchar2(100)  NOT NULL,
    admin_cod_secc varchar2(11)  NOT NULL,
    admin_cod_sede varchar2(5)  NOT NULL,
    admin_creado date  NOT NULL,
    admin_actualizado date  NULL,
    admin_imagen varchar2(255)  NULL,
    admin_password varchar2(255)  NOT NULL,
    admin_disponibilidad integer DEFAULT 1,
    CONSTRAINT tbl_administradores_transf_pk PRIMARY KEY (admin_id)
) ;

-- Table: tbl_encargados_transf
CREATE TABLE tbl_encargados_transf (
    e_transferencia_asignada varchar2(255)  NOT NULL,
    e_admin_encargado varchar2(20)  NOT NULL,
    e_fecha_asignacion date  NOT NULL,
    e_admin_asignador varchar2(20)  NOT NULL
) ;

-- Table: tbl_equivalencias_transf
CREATE TABLE tbl_equivalencias_transf (
    equiv_materia_vista_id varchar2(255)  NOT NULL,
    equiv_homologacion_id varchar2(255)  NOT NULL
) ;

-- Table: tbl_homologaciones_cun_transf
CREATE TABLE tbl_homologaciones_cun_transf (
    h_id varchar2(255)  NOT NULL,
    h_nombre varchar2(255)  NOT NULL,
    h_creditos integer  NOT NULL,
    h_cod_modalidad varchar2(6)  NOT NULL,
    h_cod_secc varchar2(11)  NOT NULL,
    h_cod_programa varchar2(40)  NOT NULL,
    h_cod_plan varchar2(125)  NOT NULL,
    h_transferencia_id varchar2(255)  NOT NULL,
    h_cod_sede varchar2(5)  NOT NULL,
    CONSTRAINT tbl_homologaciones_cun_tran_pk PRIMARY KEY (h_id)
) ;

-- Table: tbl_materias_vistas
CREATE TABLE tbl_materias_vistas (
    m_id varchar2(255)  NOT NULL,
    m_nombre varchar2(255)  NOT NULL,
    m_creditos integer  NOT NULL,
    m_institucion varchar2(255)  NOT NULL,
    m_programa varchar2(255)  NOT NULL,
    m_transferencia_id varchar2(255)  NOT NULL,
    m_modalidad varchar2(255)  NOT NULL,
    CONSTRAINT tbl_materias_vistas_pk PRIMARY KEY (m_id)
) ;

-- Table: tbl_transferencias_transf
CREATE TABLE tbl_transferencias_transf (
    t_id varchar2(255)  NOT NULL,
    t_estado varchar2(20)  DEFAULT 'Inicial',
    t_tipo varchar2(50)  NOT NULL,
    t_creado date  NOT NULL,
    t_actualizado date  NULL,
    t_cod_modalidad varchar2(6)  NOT NULL,
    t_cod_secc varchar2(11)  NOT NULL,
    t_cod_sede varchar2(5)  NOT NULL,
    t_cod_programa varchar2(40)  NOT NULL,
    t_cod_plan varchar2(125)  NOT NULL,
    t_usuario_id varchar2(20)  NOT NULL,
    t_notas varchar2(255)  NULL,
    t_transf_carta varchar2(255)  NOT NULL,
    t_nmaf05 varchar2(255)  NULL,
    t_nmaf06 varchar2(255)  NULL,
    t_nmaf15 varchar2(255)  NULL,
    t_archivo_aprobado varchar2(255)  default 'ninguno',
    t_borrado date  NOT NULL,
    CONSTRAINT tbl_transferencias_transf_pk PRIMARY KEY (t_id)
) ;

-- Table: tbl_usuarios_transf
CREATE TABLE tbl_usuarios_transf (
    u_id varchar2(20)  NOT NULL,
    u_nombres varchar2(255)  NOT NULL,
    u_apellidos varchar2(255)  NOT NULL,
    u_email varchar2(50)  NOT NULL,
    u_telefono varchar2(50)  NOT NULL,
    u_institucion_origen varchar2(255)  NOT NULL,
    u_programa_origen varchar2(255)  NOT NULL,
    u_creado date  NOT NULL,
    u_actualizado date  NULL,
    u_imagen varchar2(255)  NULL,
    u_password varchar2(255)  NOT NULL,
    CONSTRAINT tbl_usuarios_transf_pk PRIMARY KEY (u_id)
) ;

-- foreign keys
-- Reference: tbl_encargados_transf_tbl_administradores_transf (table: tbl_encargados_transf)
ALTER TABLE tbl_encargados_transf ADD CONSTRAINT tbl_encargados_transf_tbl_administradores_transf
    FOREIGN KEY (e_admin_encargado)
    REFERENCES tbl_administradores_transf (admin_id);

-- Reference: tbl_encargados_transf_tbl_transferencias_transf (table: tbl_encargados_transf)
ALTER TABLE tbl_encargados_transf ADD CONSTRAINT tbl_encargados_transf_tbl_transferencias_transf
    FOREIGN KEY (e_transferencia_asignada)
    REFERENCES tbl_transferencias_transf (t_id);

-- Reference: tbl_equivalencias_transf_tbl_homologaciones_cun_transf (table: tbl_equivalencias_transf)
ALTER TABLE tbl_equivalencias_transf ADD CONSTRAINT tbl_equivalencias_transf_tbl_homologaciones_cun_transf
    FOREIGN KEY (equiv_homologacion_id)
    REFERENCES tbl_homologaciones_cun_transf (h_id);

-- Reference: tbl_equivalencias_transf_tbl_materias_vistas (table: tbl_equivalencias_transf)
ALTER TABLE tbl_equivalencias_transf ADD CONSTRAINT tbl_equivalencias_transf_tbl_materias_vistas
    FOREIGN KEY (equiv_materia_vista_id)
    REFERENCES tbl_materias_vistas (m_id);

-- Reference: tbl_homologaciones_cun_transf_tbl_transferencias_transf (table: tbl_homologaciones_cun_transf)
ALTER TABLE tbl_homologaciones_cun_transf ADD CONSTRAINT tbl_homologaciones_cun_transf_tbl_transferencias_transf
    FOREIGN KEY (h_transferencia_id)
    REFERENCES tbl_transferencias_transf (t_id);

-- Reference: tbl_materias_vistas_tbl_transferencias_transf (table: tbl_materias_vistas)
ALTER TABLE tbl_materias_vistas ADD CONSTRAINT tbl_materias_vistas_tbl_transferencias_transf
    FOREIGN KEY (m_transferencia_id)
    REFERENCES tbl_transferencias_transf (t_id);

-- Reference: tbl_transferencias_transf_tbl_usuarios_transf (table: tbl_transferencias_transf)
ALTER TABLE tbl_transferencias_transf ADD CONSTRAINT tbl_transferencias_transf_tbl_usuarios_transf
    FOREIGN KEY (t_usuario_id)
    REFERENCES tbl_usuarios_transf (u_id);

-- End of file.
