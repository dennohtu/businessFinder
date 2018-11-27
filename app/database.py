##This class is meant to mimic a normal database
##It is therefore NOT a real database object class
class User(object):
    def __init__(self, email, username, password):
        self.__email = email
        self.__username = username
        self.__password = password
    
    def printEmail(self):
        return self.__email
    
    def printUsername(self):
        return self.__username

    def printPassword(self):
        return self.__password
##Used to create a business object
##data returned will be in dictionary format using returnBusiness() function
class Business(object):
    def __init__(self, bName, userEmail, bDesc):
        self.bizName = bName
        self.userEmail = userEmail
        self.description = bDesc
        self.location = []
        self.category = []
        self.reviews = []
    
    def returnBusiness(self):
        business = {"name":self.bizName, "email":self.userEmail, "description":self.description,
            "location":self.location, "category":self.category, "reviews":self.reviews}
        return business

    def addItem(self, category, data):
        if category is 'location':
            self.location.append(data)
        elif category is 'category':
            self.category.append(data)
        elif category is 'reviews':
            self.reviews.append(data)

    def delItem(self, category, data):
        if category is 'location':
            for subdict in self.location:
                if subdict.get('id') is data:
                    self.location.remove(subdict)
        elif category is 'category':
            for subdict in self.category:
                if subdict.get('id') is data:
                    self.location.remove(subdict)
        elif category is 'reviews':
            for subdict in self.reviews:
                if subdict.get('id') is data:
                    self.location.remove(subdict)

##Creates a category object
#Returns a dictionary with id and category to be added to the business
class Category(object):
    def __init__(self, catId, category):
        self.id = catId
        self.category = category

    def returnCategory(self):
        return {"id":self.id, "category":self.category}

##Creates a location object
#Returns a dictionary to be added to the business
class Location(object):
    def __init__(self, locId, businessId, county, region, location):
        self.id = locId
        self.businessId = businessId
        self.county = county
        self.region = region
        self.location = location
    
    def returnLoction(self):
        location = {"id":self.id, "business_id":self.businessId, "county":self.county, "region":self.region,
            "location":self.location}
        return location

##Creates a category object
#Returns a dictionary to be added to the business
class Review(object):
    def __init__(self, reviewId, businessId, email, message, stars):
        self.id = reviewId
        self.businessId = businessId
        self.email = email
        self.message = message
        self.stars = stars

    def returnReview(self):
        review = {"id":self.id, "business_id":self.businessId, "email":self.email,
            "message":self.message, "stars":self.stars}
        return review
