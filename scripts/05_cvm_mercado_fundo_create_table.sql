create table if not exists tb_cvm_mercado_fundo 
(
cd_cnpj_fundo				text 	not null,				        --cnpj_fundo
dt_fechamento		        date 	not null,						--dt_comptc
vl_carteira			        float 	not null,						--vl_total
vl_cota		                float	not null,						--vl_quota
vl_patrimonio		        float	not null,						--vl_patrim_liq
vl_captcao_dia			    float	not null,						--captc_dia
vl_resgate_dia              float	not null,						--resg_dia
vl_quantidade_cotista	    int	    not null,						--nr_cotst
constraint pk_tb_cvm_mercado_fundo primary key (cd_cnpj_fundo, dt_fechamento)
)