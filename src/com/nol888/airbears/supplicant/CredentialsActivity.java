package com.nol888.airbears.supplicant;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class CredentialsActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_credentials);
		
		overridePendingTransition(R.anim.slide_in_up, R.anim.hold);
		
		Button btnSave = (Button) findViewById(R.id.btnSave);
		btnSave.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				// save/update calnet account
				
			}
		});
    }
    
    @Override
	protected void onPause() {
		super.onPause();

		overridePendingTransition(R.anim.hold, R.anim.slide_out_down);
	}
    
}
