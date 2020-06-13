/* JS Document */

/******************************

[Table of Contents]

1. Vars and Inits
2. Set Header
3. Init Search
4. Init Menu
5. Init Isotope


******************************/


$(document).ready(function()
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var header = $('.header');
	var hambActive = false;
	var menuActive = false;

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	initSearch();
	initMenu();
	initIsotope();

	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if($(window).scrollTop() > 100)
		{
			header.addClass('scrolled');
		}
		else
		{
			header.removeClass('scrolled');
		}
	}

	/* 

	3. Init Search

	*/

	function initSearch()
	{
		if($('.search').length && $('.search_panel').length)
		{
			var search = $('.search');
			var panel = $('.search_panel');

			search.on('click', function()
			{
				panel.toggleClass('active');
			});
		}
	}

	/* 

	4. Init Menu

	*/

	function initMenu()
	{
		if($('.hamburger').length)
		{
			var hamb = $('.hamburger');

			hamb.on('click', function(event)
			{
				event.stopPropagation();

				if(!menuActive)
				{
					openMenu();
					
					$(document).one('click', function cls(e)
					{
						if($(e.target).hasClass('menu_mm'))
						{
							$(document).one('click', cls);
						}
						else
						{
							closeMenu();
						}
					});
				}
				else
				{
					$('.menu').removeClass('active');
					menuActive = false;
				}
			});

			//Handle page menu
			if($('.page_menu_item').length)
			{
				var items = $('.page_menu_item');
				items.each(function()
				{
					var item = $(this);

					item.on('click', function(evt)
					{
						if(item.hasClass('has-children'))
						{
							evt.preventDefault();
							evt.stopPropagation();
							var subItem = item.find('> ul');
						    if(subItem.hasClass('active'))
						    {
						    	subItem.toggleClass('active');
								TweenMax.to(subItem, 0.3, {height:0});
						    }
						    else
						    {
						    	subItem.toggleClass('active');
						    	TweenMax.set(subItem, {height:"auto"});
								TweenMax.from(subItem, 0.3, {height:0});
						    }
						}
						else
						{
							evt.stopPropagation();
						}
					});
				});
			}
		}
	}

	function openMenu()
	{
		var fs = $('.menu');
		fs.addClass('active');
		hambActive = true;
		menuActive = true;
	}

	function closeMenu()
	{
		var fs = $('.menu');
		fs.removeClass('active');
		hambActive = false;
		menuActive = false;
	}

	
	/* 

	5. Init Isotope

	*/

	function initIsotope()
	{
		var sortingButtons = $('.product_sorting_btn');
		var sortNums = $('.num_sorting_btn');

		if($('.product_grid').length)
		{
			var grid = $('.product_grid').isotope({
				itemSelector: '.product',
				layoutMode: 'fitRows',
				fitRows:
				{
					gutter: 30
				},
	            getSortData:
	            {
	            	price: function(itemElement)
	            	{
	            		var priceEle = $(itemElement).find('.product_price').text().replace( '$', '' );
	            		return parseFloat(priceEle);
	            	},
	            	name: '.product_name',
	            	stars: function(itemElement)
	            	{
	            		var starsEle = $(itemElement).find('.rating');
	            		var stars = starsEle.attr("data-rating");
	            		return stars;
	            	}
	            },
	            animationOptions:
	            {
	                duration: 750,
	                easing: 'linear',
	                queue: false
	            }
	        });

	        // Sort based on the value from the sorting_type dropdown
	        sortingButtons.each(function()
	        {
	        	$(this).on('click', function()
	        	{
	        		var parent = $(this).parent().parent().find('.sorting_text');
		        		parent.text($(this).text());
						var option = $(this).attr('data-isotope-option');
						var category_id = $(this).attr('data-category') 
						var url = '/sort-product/';
						console.log(option)
						$.ajax({
							type:"POST",
							url:url,
							data:{'sort':option,'category':category_id},
							success: function(data) {
								console.log(data)
								for (var i=0; i<data.length ; i++){
									console.log(data[i].fields.price);
								}
								SortPage(data)
							}
						})
	        	});
	        });
		}
	}

	function SortPage(data) {
		var product_grid = document.getElementsByClassName('product')
		for (var i =0; i < product_grid.length; i++){
			product_grid[i].querySelector('.product_title a').innerHTML = data[i].fields.name;
			product_grid[i].querySelector('.product_price').innerHTML = ConvertToVND(data[i].fields.price);
			product_grid[i].querySelector('.product_image img').src = '/media/' + data[i].fields.image;
			product_grid[i].querySelector('.product_image').setAttribute('onclick',"location.href="+"'/"+data[i].fields.slug+"';");
			product_grid[i].querySelector('.update-cart').setAttribute('data-product',data[i].pk)
		}
	}
	function ConvertToVND(price) {
		price = price.split("")
		var result = '';
		var count = 0;
		while ( price.length != 0){
			result += price.pop()
			count += 1
			if (count % 3 ==0) {
				result += ','
			}
		}
		if (result[-1] == ',') { result = result.slice(0,-1)}
		return 'VND ' + result.split("").reverse().join("");

	}
	/* 

	6. Setting Ajax CSRF TOKEN

	*/
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

});

