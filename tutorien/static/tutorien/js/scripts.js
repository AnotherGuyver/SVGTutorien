$(document).ready(function(){

  	$('body').bind('click',
  		function(e){
  			if( $(e.target).is('#log-in-link')){
  				$('#log-in-li').fadeIn('fast');
          $('#log-out-li').fadeIn('fast');
        }
        else if ( !$(e.target).parents().is('#log-out-li') && !$(e.target).parents().is('#log-in-li') ){
          $('#log-out-li').fadeOut('fast');
  				$('#log-in-li').fadeOut('fast');
  			}

  			
  		}
  	)

    $('#date').datepicker();

    $("#add-date").click(function(){
      $('.date-info').last().after('<div class="date-info"><input type="text" id="date" class="time-input datepicker" placeholder="Tag" class="time-input"><input type="text" id="room" placeholder="Raum" class="time-input"><input type="text" id="duration" placeholder="Dauer" class="time-input"><a href="javascript:" id="add-date"><img src="static/tutorien/images/-.png" alt=""></a></div>');
    });

    $('.tutorium-div').each(function(i, e){
      console.log(e);
      $('.arrow-a',e).click(function(){
        if( (parseInt( $(e).height() )+60)==290 ){
          console.log($(e).height())
          $(e).animate({'min-height':'880px'});
          $('div',this).removeClass('arrow-down').addClass('arrow-up');
          $('.tut-description-short',e).slideUp();
          $('.tut-extended',e).slideDown();
        } else {
          console.log($(e).height())
          $(e).animate({'min-height':'290px'});
          $('div',this).removeClass('arrow-up').addClass('arrow-down');
          $('.tut-description-short',e).slideDown();
          $('.tut-extended',e).slideUp();
        }
      });

      $('.alle-teilnehmer', e).click(function(){
        var l = $('.all-users', e);
        var button = $(this);
        var x = $(button).position().left;
        var y = $(button).position().top;
        $(l).css(
          {'left':x + $(button).width()+10, 'top':y - $(l).height()/2 - 15}
        );
        $('.all-users', e).show('fast');
      })

      $('.close', e).click(function(){
        $('.all-users', e).hide('fast');
      })
    });
});