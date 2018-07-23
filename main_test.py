import json
import time
import os, sys,random
import unittest, xmlrunner
from api_calls import Apicalls
from rmqDatabase import RmqDatabase
import rmqUtil
import arrow
from datetime import timedelta

class TestCase(unittest.TestCase):
    api_obj = Apicalls()
    c_month = arrow.get().month
    c_year = arrow.get().year
    if c_month < 10:
        c_month = '0'+str(c_month)
    tablename_pings= 'pings_{}_{}'.format(c_year,c_month)
    tablename_mtSummaries= 'mt_summaries_{}_{}'.format(c_year,c_month)
    tablename_mtStats= 'mt_stats_{}_{}'.format(c_year,c_month)
    tablename_subm= 'subm_{}_{}'.format(c_year,c_month)

    def test_users(self):
        res_api = self.api_obj.get("/v1/users?")
        print "\n Users data Response Code : ",res_api        
        print "\n Users data : ",res_api.json()
        self.assertIn('username', res_api.json())
        self.assertEqual(res_api.status_code, 200)
        self.assertEqual(res_api.json()['username'], 'esvtbeammap')

    def test_connectivity(self):
        print "\n Requested URL:","/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/connectivity?"
        res_api = self.api_obj.get("/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/connectivity?")
        print "\n Connectivity Response Code:",res_api
        print "\n Connectivity Data:",res_api.json()
        self.assertEqual(res_api.status_code, 200)
        self.assertEqual(res_api.json()[0]['ifc'], 'good')
         
    def test_ping(self):
        res_api = self.api_obj.get("/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/ping?")
        print "\n Ping Response Code : ",res_api
        #print "\n Ping data : ",res_api.json()
        self.assertEqual(res_api.status_code, 200)
        self.assertEqual(res_api.json()[0]['ifc_success'], 100)
        self.assertEqual(res_api.json()[0]['ifc_success'], 100)

    def test_modemdatarate(self):
        res_api = self.api_obj.get("/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/modemdatarate?")
        print "\n ModemData Response Code : ",res_api
        print "\n ModemData : ",res_api.json() 
        self.assertEqual(res_api.status_code, 200)

    def test_events(self):
        print "\n Requested URL:","/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.times['depart_time'])+"/"+rmqUtil.epoch_to_tstamp(self.times['arrival_time'])+"/events?"
        res_api = self.api_obj.get("/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.times['depart_time'])+"/"+rmqUtil.epoch_to_tstamp(self.times['arrival_time'])+"/events?")
        print "\n Events data Response Code : ",res_api
        print "\n Events data : ",res_api.json()
        self.assertEqual(res_api.status_code, 200)
        self.assertEqual(res_api.json()[0]['eventtype'], 'departure')
        self.assertEqual(res_api.json()[0]['textdisplay'], 'KCRQ')
        self.assertEqual(res_api.json()[0]['location'], 'Mc Clellan-Palomar')   

    def test_beams(self):
        res_api = self.api_obj.get("/v1/timeline/"+self.tail+"/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/beams?")
        print "\n Beams data Response Code : ",res_api
        print "\n Beams data : ",res_api.json()
        self.assertEqual(res_api.status_code, 200)

    def test_tails(self):
        res_api = self.api_obj.get("/v1/tails?ids=N108QA,N014VX,N135VX,N128VX")
        print "\n Tails data Response Code : ",res_api
        print "\n Tails data : ",res_api.json()
        self.assertEqual(res_api.status_code, 200)
            
    def test_neg_Users(self):
        res_api = self.api_obj.get("/v1/usrs")
        print "\n Response Code invalid URL : ",res_api                
        self.assertEqual(res_api.status_code, 404)
        
    def test_neg_connectivity_1(self):
        res_api = self.api_obj.get("/v1/timeline/"+self.tail+"/"+str(self.ascend_time.timestamp)+"/"+str(self.descend_time.timestamp)+"/connectivity?")
        print "\n Requested URL:","/v1/timeline/"+self.tail+"/"+str(self.ascend_time.timestamp)+"/"+str(self.descend_time.timestamp)+"/connectivity?"
        print "\n Response Code invalid time : ",res_api                
        self.assertEqual(res_api.status_code, 400)

    def test_neg_connectivity_2(self):
        res_api = self.api_obj.get("/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/connectivity?")
        print "\n Requested URL:","/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/connectivity?"
        print "\n Response Code invalid Tail ID : ",res_api                
        self.assertEqual(res_api.status_code, 204)

    def test_neg_modemdatarate(self):
        res_api = self.api_obj.get("/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/modemdatarate?")        
        print "\n Requested URL:","/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/modemdatarate?"
        print "\n Response Code invalid Tail ID : ",res_api                
        self.assertEqual(res_api.status_code, 204)

    def test_neg_events(self):
        res_api = self.api_obj.get("/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.times['depart_time'])+"/"+rmqUtil.epoch_to_tstamp(self.times['arrival_time'])+"/events?")
        print "\n Requested URL:","/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.times['depart_time'])+"/"+rmqUtil.epoch_to_tstamp(self.times['arrival_time'])+"/events?"
        print "\n Response Code invalid Tail ID : ",res_api                
        self.assertEqual(res_api.status_code, 204)

    def test_neg_beams(self):
        res_api = self.api_obj.get("/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/beams?")
        print "\n Requested URL:","/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/beams?"
        print "\n Response Code invalid Tail ID : ",res_api                
        self.assertEqual(res_api.status_code, 204)

    def test_neg_ping(self):
        res_api = self.api_obj.get("/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/ping?")
        print "\n Requested URL:","/v1/timeline/INVALID/"+rmqUtil.epoch_to_tstamp(self.ascend_time.timestamp)+"/"+rmqUtil.epoch_to_tstamp(self.descend_time.timestamp)+"/ping?"
        print "\n Response Code invalid Tail ID : ",res_api                
        self.assertEqual(res_api.status_code, 400)

    def test_neg_tails(self):          
        res_api = self.api_obj.get("/v1/tails?ids=INVALID")
        print "\n Requested URL:","/v1/tails?ids=INVALID"
        print "\n Response Code invalid Tail ID Tails endpoint: ",res_api                
        self.assertEqual(res_api.status_code, 204)

    def test_neg_tails_1(self):          
        res_api = self.api_obj.get("/v1/tails?ids=N108QA,INVALID,N128VX")
        print "\n Requested URL:","/v1/tails?ids=N108QA,INVALID,N128VX"
        print "\n Response Code invalid Tail ID Tails endpoint: ",res_api                
        self.assertEqual(res_api.status_code, 200)

    def test_aircraftlist(self):          
        res_api = self.api_obj.get("/v1/live/aircraftlist?")
        print "\n Requested URL:","/v1/live/aircraftlist?"
        print "\n aircraftlist data : ",res_api.json()       
        print "\n Response Code valid endpoint aircraftlist : ",res_api                
        self.assertEqual(res_api.status_code, 200)
        self.assertEqual(res_api.json()['features'][0]['geometry']['type'], 'Point')

    def test_neg1_aircraftlist(self):          
        res_api = self.api_obj.get("/v1/live/aircraftlists?")
        print "\n Requested URL:","/v1/live/aircraftlists?"
        print "\n Response Code invalid endpoint aircraftlists : ",res_api
        self.assertEqual(res_api.status_code, 404)

    def test_flight_details(self):          
        res_api = self.api_obj.get("/v1/live/"+self.tail+"/"+"flightdetails?")
        print "\n Requested URL:","/v1/live/"+self.tail+"/"+"flightdetails?"
        print "\n Response Code for Flight Details : ",res_api
        self.assertEqual(res_api.status_code, 200)

    def test_neg1_flight_details(self):          
        res_api = self.api_obj.get("/v1/live/INVALID/flightdetails?")
        print "\n Requested URL:","/v1/live/INVALID/flightdetails?"
        print "\n Response Code Invalid Tail ID flight Details: ",res_api                
        self.assertEqual(res_api.status_code, 204)

    @classmethod
    def setUpClass(self):
        self.routing_key = ''
        self.arrival_time = arrow.utcnow()+timedelta(minutes=1)
        self.depart_time = self.arrival_time - timedelta(minutes=60)
        self.ascend_time = self.depart_time + timedelta(minutes=5)
        self.descend_time = self.arrival_time - timedelta(minutes=5)    
    
        self.times = dict(arrival_time = self.arrival_time.timestamp,
                depart_time = self.depart_time.timestamp,
                ascend_time = self.ascend_time.timestamp,
                descend_time =  self.descend_time.timestamp)
                
        self.tail_Id = dict(N101CA="N101CA",
                            N039QF="N039QF",
                            N108QA="N108QA",
                            N709JB="N709JB")
        self.tail = random.choice(self.tail_Id.keys())                
    
        # Create Database engine and connect    
        rmq_db = RmqDatabase(self.routing_key)
        self.tail_id = self.tail_Id[self.tail] 
        self.tail_map = rmqUtil.get_mt_details(rmq_db,self.tail_id)
        print 'tailmap is ',self.tail_map
        self.flight_id = "FLIGHT-{}-{}-TEST".format(self.tail_map[self.tail_id]['id'],arrow.get(self.times['depart_time']).format('YYYY-MM-DD-HH-mm'))
        print "FLight ID is  : ",self.flight_id       
        self.flights = rmqUtil.generate_flights(self.flight_id,rmq_db,self.times,self.tail_map[self.tail_id])
        rmq_db.insert('flights',self.flights,bulk=False)
        print "Flights data : {}".format(self.flights)
        
        self.pings = rmqUtil.generate_pings(rmq_db,
                            self.times['ascend_time'],
                            self.times['descend_time']+1,
                            100.00,self.tail_map[self.tail_id])
        rmq_db.insert(self.tablename_pings,self.pings,bulk=True)
        print "Total count of pings records inserted are : ",len(self.pings)

        self.mt_stats = rmqUtil.generate_mt_stats(self.flight_id,
                                             self.times['ascend_time'],
                                             self.times['descend_time']+1,
                                             self.tail_map[self.tail_id])
        rmq_db.insert(self.tablename_mtStats,self.mt_stats,bulk=False)

        self.mt_summaries = rmqUtil.generate_mt_summaries(self.times['depart_time'],
                                                     self.times['arrival_time']+1,
                                                     self.tail_map[self.tail_id])
        print "Inserting in mt_summaries"
        rmq_db.insert(self.tablename_mtSummaries,self.mt_summaries,bulk=True)

        ho_time = self.times['ascend_time']+300
        beam = {'to':1110,'from':1111}
        sat = {'to':6,'from':6}
        self.ho = rmqUtil.generate_ho(ho_time,self.tail_map[self.tail_id],beam,sat)
        print "Inserting in handover"
        rmq_db.insert('handovers',self.ho)

        self.subm = rmqUtil.generate_subm(self.times['depart_time'],self.times['arrival_time']+1,self.tail_map[self.tail_id])
        print "Inserting in subms"
        rmq_db.insert(self.tablename_subm,self.subm)
        
    @classmethod
    def tearDownClass(self):
        #Create Database engine and connect
        rmq_db = RmqDatabase(self.routing_key)
        self.tail_id = self.tail_Id[self.tail] 
        rmq_db.delete('flights',self.flights,'fa_flight_id')      
        rmq_db.delete(self.tablename_pings,self.pings,'mt_id')
        rmq_db.delete(self.tablename_mtStats,self.mt_stats,'mt_id')
        rmq_db.delete(self.tablename_mtSummaries,self.mt_summaries,'mt_id',**{'source': 'TEST DATA','tstamp':'> CURRENT_TIMESTAMP - INTERVAL \'10 minutes\''})
        rmq_db.delete('handovers',self.ho,'mt_id',**{'source': 'TEST DATA','tstamp':'> CURRENT_TIMESTAMP - INTERVAL \'10 minutes\''})
        rmq_db.delete(self.tablename_subm,self.subm,'tail_id',**{'source': 'TEST DATA','tstamp':'> CURRENT_TIMESTAMP - INTERVAL \'10 minutes\''})
        res_api = self.api_obj.delete("/v1/users?")      
       
def main():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestCase))
    result = xmlrunner.XMLTestRunner(output='test-results').run(suite)

    if (result.failures > 0):
        sys.exit(1)

    sys.exit(0)

# Call main with -1 args
if __name__ == "__main__":
    main()