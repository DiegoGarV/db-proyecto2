CREATE TABLE alimentos (
    id_alimento          INTEGER NOT NULL,
    tipo_alimento        VARCHAR(10),
    nombre_alimento      VARCHAR(100),
    descripcion_alimento VARCHAR(200),
    precio_alimento      FLOAT(2)
);

ALTER TABLE alimentos ADD CONSTRAINT alimentos_pk PRIMARY KEY ( id_alimento );

CREATE TABLE areas (
    id_area           INTEGER NOT NULL,
    nombre_area       VARCHAR(50) NOT NULL,
    permite_fumadores VARCHAR(3)
);

ALTER TABLE areas ADD CONSTRAINT areas_pk PRIMARY KEY ( id_area );

CREATE TABLE clientes (
    nit_cliente       INTEGER NOT NULL,
    nombre_cliente    VARCHAR(100),
    direccion_cliente VARCHAR(100)
);

ALTER TABLE clientes ADD CONSTRAINT clientes_pk PRIMARY KEY ( nit_cliente );

CREATE TABLE encuestas_servicio (
    id_encuesta           INTEGER NOT NULL,
    puntuacion_amabilidad INTEGER,
    puntuacion_exactitud  INTEGER
);

ALTER TABLE encuestas_servicio ADD CONSTRAINT encuestas_servicio_pk PRIMARY KEY ( id_encuesta );

CREATE TABLE mesas (
    id_mesa           INTEGER NOT NULL,
    cantidad_personas INTEGER,
    movilidad         VARCHAR(3),
    id_area     INTEGER NOT NULL
);

ALTER TABLE mesas ADD CONSTRAINT mesas_pk PRIMARY KEY ( id_mesa );

CREATE TABLE meseros (
    id_personal   INTEGER NOT NULL,
    id_area INTEGER NOT NULL
);

ALTER TABLE meseros ADD CONSTRAINT meseros_pk PRIMARY KEY ( id_personal );

CREATE TABLE ordenes (
    id_orden                       INTEGER NOT NULL,
    estado_orden                   VARCHAR(10),
    total_orden                    FLOAT(2),
    porcentaje_propina             INTEGER,
    id_mesa                  INTEGER NOT NULL,
    nit_cliente           		   INTEGER NOT NULL,
    id_personal          		   INTEGER NOT NULL,
    id_encuesta 				   INTEGER NOT NULL
);

ALTER TABLE ordenes ADD CONSTRAINT ordenes_pk PRIMARY KEY ( id_orden );

CREATE TABLE pagos (
    id_pago     INTEGER NOT NULL,
    metodo_pago VARCHAR(50)
);

ALTER TABLE pagos ADD CONSTRAINT pagos_pk PRIMARY KEY ( id_pago );

CREATE TABLE pagos_ordenes (
    monto            FLOAT(2),
    id_orden 		 INTEGER NOT NULL,
    id_pago    		 INTEGER NOT NULL
);

CREATE TABLE pedidos (
    cantidad              INTEGER,
    id_alimento INTEGER NOT NULL,
    id_orden      INTEGER NOT NULL
);

CREATE TABLE personal (
    id_personal      INTEGER NOT NULL,
    nombre_personal  VARCHAR(100),
    posicion_laboral VARCHAR(100)
);

ALTER TABLE personal ADD CONSTRAINT personal_pk PRIMARY KEY ( id_personal );

CREATE TABLE quejas (
    id_queja              INTEGER NOT NULL,
    fecha_queja           DATE,
    motivo_queja          VARCHAR(300),
    puntuacion_gravedad   INTEGER,
    nit_cliente  		  INTEGER NOT NULL,
    id_personal  		  INTEGER NOT NULL,
    id_alimento 		  INTEGER NOT NULL
);

ALTER TABLE quejas ADD CONSTRAINT quejas_pk PRIMARY KEY ( id_queja );

ALTER TABLE mesas
    ADD CONSTRAINT mesas_areas_fk FOREIGN KEY ( id_area )
        REFERENCES areas ( id_area );

ALTER TABLE meseros
    ADD CONSTRAINT meseros_areas_fk FOREIGN KEY ( id_area )
        REFERENCES areas ( id_area );

ALTER TABLE meseros
    ADD CONSTRAINT meseros_personal_fk FOREIGN KEY ( id_personal )
        REFERENCES personal ( id_personal );

ALTER TABLE ordenes
    ADD CONSTRAINT ordenes_clientes_fk FOREIGN KEY ( nit_cliente )
        REFERENCES clientes ( nit_cliente );

ALTER TABLE ordenes
    ADD CONSTRAINT ordenes_encuestas_servicio_fk FOREIGN KEY ( id_encuesta )
        REFERENCES encuestas_servicio ( id_encuesta );

ALTER TABLE ordenes
    ADD CONSTRAINT ordenes_mesas_fk FOREIGN KEY ( id_mesa )
        REFERENCES mesas ( id_mesa );

ALTER TABLE ordenes
    ADD CONSTRAINT ordenes_meseros_fk FOREIGN KEY ( id_personal )
        REFERENCES meseros ( id_personal );

ALTER TABLE pagos_ordenes
    ADD CONSTRAINT pagos_ordenes_ordenes_fk FOREIGN KEY ( id_orden )
        REFERENCES ordenes ( id_orden );

ALTER TABLE pagos_ordenes
    ADD CONSTRAINT pagos_ordenes_pagos_fk FOREIGN KEY ( id_pago )
        REFERENCES pagos ( id_pago );

ALTER TABLE pedidos
    ADD CONSTRAINT pedidos_alimentos_fk FOREIGN KEY ( id_alimento )
        REFERENCES alimentos ( id_alimento );

ALTER TABLE pedidos
    ADD CONSTRAINT pedidos_ordenes_fk FOREIGN KEY ( id_orden )
        REFERENCES ordenes ( id_orden );

ALTER TABLE quejas
    ADD CONSTRAINT quejas_alimentos_fk FOREIGN KEY ( id_alimento )
        REFERENCES alimentos ( id_alimento );

ALTER TABLE quejas
    ADD CONSTRAINT quejas_clientes_fk FOREIGN KEY ( nit_cliente )
        REFERENCES clientes ( nit_cliente );

ALTER TABLE quejas
    ADD CONSTRAINT quejas_personal_fk FOREIGN KEY ( id_personal )
        REFERENCES personal ( id_personal );
		
CREATE OR REPLACE FUNCTION verificar_estado_orden()
RETURNS TRIGGER AS $$
BEGIN
    DECLARE
        estado_orden_actual VARCHAR(50);
    BEGIN
        SELECT estado_orden INTO estado_orden_actual
        FROM Ordenes
        WHERE id_orden = NEW.id_orden;

        IF estado_orden_actual ILIKE 'cerrado' THEN
            RAISE EXCEPTION 'No se puede agregar más comidas a una orden cerrada';
        END IF;
        
        RETURN NEW;
    END;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_estado_orden_trigger
BEFORE INSERT ON Pedidos
FOR EACH ROW
EXECUTE FUNCTION verificar_estado_orden();