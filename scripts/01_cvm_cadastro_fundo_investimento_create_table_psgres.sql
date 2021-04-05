--drop table marketdata.tb_cvm_cadastro_fundo_investimento;

create table if not exists marketdata.tb_cvm_cadastro_fundo_investimento
	(
	id_fundo 					integer 		not null,
	tp_fundo 					text			not null,					--TP_FUNDO
	cd_cnpj_fundo				varchar(50) 	not null,				    --CNPJ_FUNDO
	cd_cvm						integer 		null,				        --CD_CVM
	nm_denom_social_fundo		varchar(100) 	not null,					--DENOM_SOCIAL
	dt_registro_fundo 			date 			null,						--DT_REG
	dt_constituicao_fundo		date			null,						--DT_CONST
	dt_cancelamento_fundo		date			null,						--DT_CANCEL
	cd_situacao_fundo			varchar(50)		not null,					--SIT
	dt_inicio_situacao_fundo	date			not null,					--DT_INI_SIT
	dt_inicio_atividade	        date			null,						--DT_INI_ATIV
	dt_inicio_exec_soc_fundo	date			null,						--DT_INI_EXERC
	dt_fim_exec_soc_fundo		date			null,						--DT_FIM_EXERC
	nm_classe                   varchar(50)		null,                       --CLASSE
	dt_inicio_classe	        date			null,						--DT_INI_CLASSE
	nm_indicador_rentabilidade	varchar(100) 	null,                       --RENTAB_FUNDO
	tp_condominio               varchar(100)    null,                       --CONDOM
	es_fundo_cota               varchar(3)    	null,                       --FUNDO_COTAS
	es_fundo_exclusivo          varchar(3)    	null,                       --FUNDO_EXCLUSIVO
	es_tributacao_longo_prazo   varchar(3)    	null,                       --TRIB_LPRAZO
	es_investidor_qualificado   varchar(3)    	null,                       --INVEST_QUALIF
	es_entidade_investimento	varchar(3)    	null,                       --INVEST_QUALIF
	vl_taxa_performance         real   			null,                       --TAXA_PERFM
	tx_info_performance         varchar(400)	null,                       --INF_TAXA_PERFM
	vl_taxa_adm         		real   			null,                       --TAXA_PERFM
	tx_info_adm         		varchar(400)	null,                       --INF_TAXA_PERFM
	vl_patrimonio_liquido       real   			null,                       --VL_PATRIM_LIQ
	dt_patrimonio_liquido       date    		null,                       --DT_PATRIM_LIQ
	nm_diretor                  varchar(100)    null,                       --DIRETOR
	cd_cnpj_admin				varchar(50) 	null,						--CNPJ_ADMIN
	nm_admin					varchar(100) 	null,						--ADMIN
	tp_pessoa_gestor			varchar(3) 		null,						--PF_PJ_GESTOR
	cd_cpf_cnpj_gestor			varchar(50) 	null,						--CPF_CNPJ_GESTOR
	nm_gestor					varchar(100) 	null,						--GESTOR
	cd_cnpj_auditor				varchar(50) 	null,						--CNPJ_AUDITOR
	nm_auditor					varchar(100) 	null,						--AUDITOR
	cd_cnpj_custodiante			varchar(50) 	null,						--CNPJ_CUSTODIANTE
	nm_custodiante				varchar(100) 	null,						--CUSTODIANTE
	cd_cnpj_controlador			varchar(50) 	null,						--CNPJ_CONTROLADOR
	nm_controlador				varchar(100) 	null						--CONTROLADOR
	,constraint pk_tb_cvm_cadastro_fundo_investimento primary key (id_fundo)
	);

	create sequence marketdata.sq_cvm_cadastro_fundo_investimento start 1 OWNED BY marketdata.tb_cvm_cadastro_fundo_investimento.id_fundo;
	
	alter table marketdata.tb_cvm_cadastro_fundo_investimento alter column id_fundo set default nextval('marketdata.sq_cvm_cadastro_fundo_investimento');
	--ALTER SEQUENCE marketdata.sq_cvm_cadastro_fundo_investimento RESTART WITH 1;