create table if not exists tb_b3_carteira_importacao
(
    id_carteira     integer         not null primary key autoincrement
    ,sg_carteira    varchar(100)    not null
    ,dt_inicio      datetime        not null    
    ,constraint uk_tb_b3_carteira_importacao_01 unique (sg_carteira,dt_inicio)
)