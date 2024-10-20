package io.openliberty.guides.rest;

import java.sql.Timestamp;
//import java.text.SimpleDateFormat;
//import java.util.Date;


public class UpTime {
    private static long ts0 = 0;
    
    public UpTime() {
	if (this.ts0 == 0) {
	    this.ts0 = System.currentTimeMillis();
	}
    }

    public long getUpTime() {
	long ts1 = (System.currentTimeMillis() - ts0)/1000;
	return ts1;
    }
}
