

$(document).ready(function(){
	var count=0; 

	 $('.modal').modal();

	// Carrega informações armazenadas
	function obtem_modelo_carregado(){
		$.get('/info', function(data){
			$('#modelo_carregado').html(
				'<li>Nome do arquivo: <strong>' + data.filename + '</strong></li>Eficiência: <strong>' + data.pontuacao.toFixed(3)*100 + ' 	%</strong></li>')
		}, 'json')
	}
	obtem_modelo_carregado();
	
	// Envia um arquivo via ajax
	var uploadObj = $("#fileuploader").uploadFile({
		url: "/dados",
		fileName:"file",
		maxFileCount: 1,
		onSuccess: function(files, data, xhr, pd){

			 obtem_modelo_carregado();

			// Evita cache da imagem
			img = $("#features_importance")
			img.attr('src', img.attr('src') + new Date().getTime());
		},
		onError: function(files,status,errMsg,pd){
		    errMsg: alert('Erro!')
		},
		allowedTypes: 'csv',
		showDelete: true,
		showStatusAfterSuccess: true,
		uploadStr: 'Enviar arquivo',
		autoSubmit: false,
		extErrorStr: 'Selecione um arquivo válido! ',
		
		afterUploadAll: function(obj){
			uploadObj.reset();
		},
		onSelect:function(files){
	       $('#modal1').modal('open');
	       
	       $('#enviar_sim').click(function(){
	       		uploadObj.startUpload();
	       });

	       $('#enviar_nao').click(function(){
	       		uploadObj.reset();
	       });

	   	},
	});

	// Carrega formulário de simulação
	$('#card_simulacao').click(function(){
			
		$.get('/simulacao', function(data){
			
			// Oculta barra progresso
  			$('.progress').hide();
			
			$.get('/static/js/template.html?v=' + Math.random(), function(template){
				
				// Oculta barra progresso
  				$('.progress').hide();

				features = data['features'];
				
				for (i = 0; i < features.length; i++){
					features[i]['index'] = i;
				}

				$('#features').empty();

				// Preenche features
				$.tmpl(template, features).appendTo('#features')			
			});
			
		}, 'json');
	});

	// Quando um range mudar calcula nota para features
	$('#form_simulacao').change(function(e){

		// Previne comportamento default do form.
		e.preventDefault();

		// Dados do formulário
		var data = $(this).serialize()

		$.post("/simulacao", data, function(data) {
  
  			$('#nota').text('Pontuação: ' + data['nota']);
  			Materialize.toast('Pontuação: ' + data.nota, 4000, 'rounded')

		},'json').fail(function(){
			console.log('Erro');
		})
	})

	// Exibe e esconde botão voltar ao topo
    $(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('a[href="#top"]').fadeIn();
        } else {
            $('a[href="#top"]').fadeOut();
        }
    });
});

