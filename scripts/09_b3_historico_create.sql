create table if not exists tb_b3_historico_pregao
(
    tp_registro             int             not null
    ,dt_pregao              datetime        not null
    ,cd_bdi                 int             not null
    ,cd_negociacao          varchar(100)    not null
    ,tp_mercado             int             not null
    ,nm_ativo               varchar(200)    not null
    ,tp_especificacao       varchar(200)    not null
    ,nr_dias_vencimento_termo int           null
    ,cd_moeda               varchar(3)      not null
    ,vl_abertura            FLOAT           not null
    ,vl_maxima              FLOAT           not null
    ,vl_minima              FLOAT           not null
    ,vl_medio               FLOAT           not null
    ,vl_ultimo              FLOAT           not null
    ,vl_melhor_compra       FLOAT           not null
    ,vl_melhor_venda        FLOAT           not null
    ,vl_total_negocio       FLOAT           not null
    ,vl_total_quantidade    FLOAT           not null
    ,vl_total_financeiro    FLOAT           not null
    ,vl_strike              FLOAT           null
    ,vl_strikeCorrection    int             null
    ,dt_vencimento          DATETIME        null
    ,vl_fator_cotacao       float           null
    ,vl_strike_usd_points   FLOAT           null
    ,cd_isin                varchar(100)    null
    ,cd_distribuicao        int             null
)