insert into tb_cvm_mercado_fundo 
			(
			cd_cnpj_fundo				
			,dt_fechamento		        
			,vl_carteira			        
			,vl_cota		                
			,vl_patrimonio		        
			,vl_captcao_dia			    
			,vl_resgate_dia              
			,vl_quantidade_cotista	    
			)
			values
			(				
			:CNPJ_FUNDO
			,:DT_COMPTC
			,:VL_TOTAL
			,:VL_QUOTA
			,:VL_PATRIM_LIQ
			,:CAPTC_DIA
			,:RESG_DIA
			,:NR_COTST
			)
			