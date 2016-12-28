// 
// Here is how to define your module 
// has dependent on mobile-angular-ui
// 
var app = angular.module('ConfPlusWebApp', [
  'ngRoute',
  'mobile-angular-ui',
  'ConfPlusWebApp.controllers',
  'ConfPlusWebApp.restServices',
  // touch/drag feature: this is from 'mobile-angular-ui.gestures.js'
  // it is at a very beginning stage, so please be careful if you like to use
  // in production. This is intended to provide a flexible, integrated and and 
  // easy to use alternative to other 3rd party libs like hammer.js, with the
  // final pourpose to integrate gestures into default ui interactions like 
  // opening sidebars, turning switches on/off ..
  'mobile-angular-ui.gestures'
]);

app.run(function($transform) {
  window.$transform = $transform;
});

// 
// You can configure ngRoute as always, but to take advantage of SharedState location
// feature (i.e. close sidebar on backbutton) you should setup 'reloadOnSearch: false' 
// in order to avoid unwanted routing.
// 
app.config(function($routeProvider) {

  $routeProvider.when('/',              							{redirectTo: '/confinfo'+defaultConfId});
  $routeProvider.when('/confinfo/:confId',        					{templateUrl: 'confinfo.html', reloadOnSearch: false}); 
  $routeProvider.when('/sesslist/:confId/:title/:type',   			{templateUrl: 'sesslist.html', reload: false, reloadOnSearch: false}); 
  $routeProvider.when('/sessiondetail/:confId/:title/:sessId',  	{templateUrl: 'sessiondetail.html', reload: true, reloadOnSearch: false}); 
  $routeProvider.when('/memberlist/:confId/:title/:type',  			{templateUrl: 'memberlist.html', reloadOnSearch: false}); 
  $routeProvider.when('/memberdetail/:confId/:title/:memId',    	{templateUrl: 'memberdetail.html', reloadOnSearch: false});
  $routeProvider.when('/companylist/:confId/:title/:type',  		{templateUrl: 'companylist.html', reloadOnSearch: false});
  $routeProvider.when('/companydetail/:confId/:title/:cmpId',   	{templateUrl: 'companydetail.html', reloadOnSearch: false});
  $routeProvider.when('/maplist/:confId/:title/:type',     			{templateUrl: 'maplist.html', reloadOnSearch: false});
  $routeProvider.when('/mapdetail/:confId/:title/:mapId',     		{templateUrl: 'mapdetail.html', reloadOnSearch: false});
  $routeProvider.when('/customlist/:confId/:title/:type',   		{templateUrl: 'customlist.html', reloadOnSearch: false});
  $routeProvider.when('/customdetail/:confId/:title/:customId', 	{templateUrl: 'customdetail.html', reloadOnSearch: false});
  $routeProvider.otherwise({redirectTo: '/confinfo/'+defaultConfId});
});

app.filter("trustHtml",function($sce){
   return function (input){
       return $sce.trustAsHtml(input); 
   } 
});

app.filter('rateURL',function(){
    return function(input, sid, uid){
		var output;
		output = input.replace("%sid%",sid);
		output = output.replace("%uid%",uid);
        return output;
    }
});

app.filter('actionURL',function(){
    return function(input){
		var output;
		output = input.replace("CPConf://detail?confid=","#/confinfo/");
        return output;
    }
});

