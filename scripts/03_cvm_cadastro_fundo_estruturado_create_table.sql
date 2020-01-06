create table if not exists tb_cvm_cadastro_fundo_estruturado
(
id_fundo 					integer not null,
tp_fundo 					text	not null,						--TP_FUNDO
cd_cnpj_fundo				text 	not null,				        --CNPJ_FUNDO
nm_denom_social_fundo		text 	not null,						--DENOM_SOCIAL
dt_registro_fundo 			date 	not null,						--DT_REG
dt_constituicao_fundo		date	not null,						--DT_CONST
dt_cancelamento_fundo		date	null,							--DT_CANCEL
cd_situacao_fundo			text	not null,						--SIT
dt_inicio_situacao_fundo	date	not null,						--DT_INI_SIT
dt_inicio_exec_soc_fundo	date	not null,						--DT_INI_EXERC
dt_fim_exec_soc_fundo		date	not null,						--DT_FIM_EXERC
cd_cnpj_admin				text 	not null,						--CNPJ_ADMIN
nm_admin					text 	not null,						--ADMIN
tp_pessoa_gestor			text 	not null,						--PF_PJ_GESTOR
cd_cpf_cnpj_gestor			text 	not null,						--CPF_CNPJ_GESTOR
nm_gestor					text 	not null,						--GESTOR
cd_cnpj_auditor				text 	not null,						--CNPJ_AUDITOR
nm_auditor					text 	not null,						--AUDITOR
constraint pk_tb_cvm_cadastro_fundo_estruturado primary key (id_fundo)
)
