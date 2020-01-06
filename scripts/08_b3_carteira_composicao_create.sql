create table if not exists tb_b3_carteira_composicao
(
    id_carteira     int not null 
    ,cd_acao        varchar(100)    not null
    ,nm_acao        varchar(200)    not null
    ,tp_acao        varchar(100)    not null
    ,qt_acao        float           not null
    ,ft_parcipacao  float           not null   
    ,constraint pk_tb_b3_carteira_composicao primary key (id_carteira,cd_acao)
    ,constraint fk_tb_b3_carteira_composicao_tb_b3_carteira_importacao foreign key (id_carteira)
        references tb_b3_carteira_importacao (id_carteira)
)