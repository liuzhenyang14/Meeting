'use strict';

	var appModule = angular.module('ConfPlusWebApp.restServices', ["ngResource"]);
	
	appModule.factory('getConfInfo', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/confInfo/:confId', {});
        }
    ]);
	
    appModule.factory('getSessList', function ($resource){
		return $resource(restUrlHead + '/sessionlist/:confId/:type/:userId', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
    });  
	
	appModule.factory('getSessDates', function ($resource){
		return $resource(restUrlHead + '/sessionDates/:confId/:type', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
	});
	
	appModule.factory('getMemberList', function ($resource){
		return $resource(restUrlHead + '/memberlist/:confId/:type', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
    }); 
	
	appModule.factory('getSessDetail', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/session/:sessId/:userId', {});
        }
    ]);
	
	appModule.factory('getMemDetail', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/member/:memId', {});
        }
    ]);
	
	appModule.factory('getCmpList', function ($resource){
		return $resource(restUrlHead + '/companylist/:confId/:type', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
    }); 

	appModule.factory('getCmpDetail', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/company/:cmpId', {});
        }
    ]);
	
	appModule.factory('getMapList', function ($resource){
		return $resource(restUrlHead + '/maplist/:confId', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
    }); 
	
	appModule.factory('getMapDetail', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/map/:mapId', {});
        }
    ]);
	
	appModule.factory('getCustomList', function ($resource){
		return $resource(restUrlHead + '/customlist/:confId/:type', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
    }); 
	
	appModule.factory('getCustomDetail', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/custominfo/:customId', {});
        }
    ]);
	
	appModule.factory('getMenuList', function ($resource){
		return $resource(restUrlHead + '/menulist/:confId', {},
		{query: {method:'GET',params:{}, isArray:true}}); 
    }); 
	
    appModule.factory('login', function($http) {
        return {
            login: function(userEmail, userPassword, $rootScope) {
				$http({
                    method: 'POST',
                    url: restUrlHead + '/login',
                    data: {email:userEmail,password:userPassword, confid:$rootScope.confId},
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'text/plain'}
                }).success(function(data){
					if(data != ""){
						$rootScope.user = data;
						$rootScope.userId = data.id;
					}else{
						$rootScope.userId = "-1";
					}
				});
            }
        };
    });
	
	appModule.factory('saveSchedule', function($http) {
        return {
            save: function(sessId, userId, attend, $scope) {
				//if(userId == null || userId == 0 || userId == -1){
				//	$scope.resMsg = 'Please login at side sliding menu to register for any session.';
				//}else{
					$http({
						method: 'POST',
						url: restUrlHead + '/saveSchedule',
						data: {sessId:sessId,userId:userId, attend:attend},
						headers: {
							'Accept': 'application/json',
							'Content-Type': 'text/plain'}
					}).success(function(data){
						if(data != ""){
							$scope.res = data;
							if($scope.res == '0'){
								$scope.session.attend = attend;
								if(attend === '1'){
									$scope.resMsg = 'You have successfully registered to this session';
									$scope.errMsg = '';
								}else if(attend === '0'){
									$scope.resMsg = 'Your session registration has been cancelled';
									$scope.errMsg = '';
								}								
							}else if($scope.res == "71"){
								$scope.errMsg = 'Failed: Schedule Conflict';
								$scope.resMsg = '';
							}else if($scope.res == "72"){
								$scope.errMsg = 'Registration failed: no seats available';
								$scope.resMsg = '';
							}else if($scope.res == "73"){
								$scope.errMsg = 'Failed: Pre-Registration Required';
								$scope.resMsg = '';
							}else{
								$scope.errMsg = 'Failed: Unknown reason, please try again later.';
								$scope.resMsg = '';
							}
						}else{
							$scope.res = '79';
							$scope.errMsg = 'Failed: Unknown reason, please try again later.';
						}
					});
				//}
            }
        };
    });
	
	/*
    Demo.factory('Attendee', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/attendees/confid/:userEmail/:confId', {} ,
                {query: {method:'GET',params:{}, isArray:true}});  
        }
    ]);*/
/*

	appModule.factory('Login', function($http) {
        return {
            login: function(userEmail, userPassword) {
                return $http.get(restUrlHead + '/userlogin/' + userEmail + '/' + userPassword);
            }
        };
    });
	
    appModule.factory('AttendeeDetail', ['$resource',
        function ($resource) {
            return $resource(restUrlHead + '/attendees/:userEmail/:confId/:attendeeId', {});
        }
    ]);

    appModule.factory('Login', function($http) {
        return {
            login: function(userEmail, confCode) {
                return $http.get(restUrlHead + '/userlogin/' + userEmail + '/' + confCode);
            }
        };
    });

    appModule.factory('SendEmail', function($http) {
        return {
            sendEmail: function(attdMessage) {
                $http({
                    method: 'POST',
                    url: restUrlHead + '/sendemail',
                    data: attdMessage,
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'text/plain'}
                });
            }
        };
    });
	*/