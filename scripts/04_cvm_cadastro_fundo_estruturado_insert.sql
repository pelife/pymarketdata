insert into tb_cvm_cadastro_fundo_estruturado 
			(
				 tp_fundo
				, cd_cnpj_fundo
				, nm_denom_social_fundo
				, dt_registro_fundo
				, dt_constituicao_fundo
				, dt_cancelamento_fundo
				, cd_situacao_fundo
				, dt_inicio_situacao_fundo
				, dt_inicio_exec_soc_fundo
				, dt_fim_exec_soc_fundo
				, cd_cnpj_admin
				, nm_admin
				, tp_pessoa_gestor
				, cd_cpf_cnpj_gestor
				, nm_gestor
				, cd_cnpj_auditor
				, nm_auditor
			)
			values
			(				
				 :TP_FUNDO
				,:CNPJ_FUNDO
				,:DENOM_SOCIAL
				,:DT_REG
				,:DT_CONST
				,:DT_CANCEL
				,:SIT
				,:DT_INI_SIT
				,:DT_INI_EXERC
				,:DT_FIM_EXERC
				,:CNPJ_ADMIN
				,:ADMIN
				,:PF_PJ_GESTOR
				,:CPF_CNPJ_GESTOR
				,:GESTOR
				,:CNPJ_AUDITOR
				,:AUDITOR
			)
			/*
			on conflict(cd_cnpj_fundo) 
				do update set 
					tp_fundo					=	excluded.tp_fundo
					,nm_denom_social_fundo		=	excluded.nm_denom_social_fundo
					,dt_registro_fundo			=	excluded.dt_registro_fundo
					,dt_constituicao_fundo		=	excluded.dt_constituicao_fundo
					,dt_cancelamento_fundo		=	excluded.dt_cancelamento_fundo
					,dt_inicio_situacao_fundo	=	excluded.dt_inicio_situacao_fundo	
					,dt_inicio_exec_soc_fundo	=	excluded.dt_inicio_exec_soc_fundo	
					,dt_fim_exec_soc_fundo		=	excluded.dt_fim_exec_soc_fundo		
					,cd_cnpj_admin				=	excluded.cd_cnpj_admin				
					,nm_admin					=	excluded.nm_admin					
					,tp_pessoa_gestor			=	excluded.tp_pessoa_gestor			
					,cd_cpf_cnpj_gestor			=	excluded.cd_cpf_cnpj_gestor		
					,nm_gestor					=	excluded.nm_gestor					
					,cd_cnpj_auditor			=	excluded.cd_cnpj_auditor			
					,nm_auditor					=	excluded.nm_auditor				
				*/