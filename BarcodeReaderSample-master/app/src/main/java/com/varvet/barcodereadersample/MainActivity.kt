//Copyright © 2019 Lucas Castanheira
//lbcastanheira@inf.ufrgs.br

package com.varvet.barcodereadersample
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Message
import android.support.v7.app.AppCompatActivity
import android.util.Log
import android.view.View
import android.widget.*
import com.google.android.gms.common.api.CommonStatusCodes
import com.google.android.gms.vision.barcode.Barcode
import com.varvet.barcodereadersample.barcode.BarcodeCaptureActivity
import java.io.InputStream
import java.lang.Exception
import java.lang.Object
import java.net.*
import android.widget.Toast



object Vlad{

    var optionsSession:List<String> =  arrayListOf("error")
}

class MainActivity : AppCompatActivity() {

    var part:String="Join"
    var sess:String="ST00"

    fun showToast(toast: String) {
        runOnUiThread { Toast.makeText(this@MainActivity, toast, Toast.LENGTH_SHORT).show() }
    }

    private fun sendGet(name_inst:String) {
//        val uri = URI("https", "sbrc.d4c.wtf", "/qr/$name_inst/$sess/$part", null) //<- anterior
        val uri = URI("http", null,"gercom.ddns.net", 8082, "/qr/$name_inst/$sess/$part", null, null)

        println("Era pra ter ido")
        val template = uri.toString()
        val connection = URL(template).openConnection() as HttpURLConnection

        try {
            val data = connection.inputStream.bufferedReader().readText()
            System.out.println(data)
            if (data.split(';')[0].toInt() == 0){
                showToast(toast = "Você fez um check-in recente. Por favor, espere "+ (30-data.split(';')[1].toInt()) +" minutos.")
            }else if (data.split(';')[0].toInt() == 1){
                showToast(toast = "Check-in realizado com sucesso")
            }
            println("Foi")
        }
        catch(e:Exception){
            println("Erro")
            System.out.println(e)
            System.out.println("AAA")
        }
        finally {
            println("Desconectado")
            connection.disconnect()
        }

    }

    lateinit var optionSession: Spinner
    lateinit var optionPart: Spinner

    private lateinit var mResultTextView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        optionPart=findViewById<Spinner>(R.id.spinnerPart)
        optionSession=findViewById<Spinner>(R.id.spinnerSession)

        Thread{

            val sessions=URL("http://gercom.ddns.net:8082/sessions").readText().split(",")
            Vlad.optionsSession = sessions

        }.start()

        while(Vlad.optionsSession.size == 1)
        {
            Thread.sleep(400)
        }

        val optionsPart= arrayOf("Join","Question","Optout")

        optionSession.adapter = ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,Vlad.optionsSession)
        optionSession.onItemSelectedListener = object : AdapterView.OnItemSelectedListener{
            override fun onNothingSelected(parent: AdapterView<*>?) {
            }

            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                sess= Vlad.optionsSession.get(position)
            }
        }

        optionPart.adapter = ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,optionsPart)
        optionPart.onItemSelectedListener = object : AdapterView.OnItemSelectedListener{
            override fun onNothingSelected(parent: AdapterView<*>?) {
                }

            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                part= optionsPart.get(position)
            }
        }
        mResultTextView = findViewById(R.id.result_textview)

        findViewById<Button>(R.id.scan_barcode_button).setOnClickListener {
            val intent = Intent(applicationContext, BarcodeCaptureActivity::class.java)
            startActivityForResult(intent, BARCODE_READER_REQUEST_CODE)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (requestCode == BARCODE_READER_REQUEST_CODE) {
            if (resultCode == CommonStatusCodes.SUCCESS) {
                if (data != null) {
                    val barcode = data.getParcelableExtra<Barcode>(BarcodeCaptureActivity.BarcodeObject)
                    val p = barcode.cornerPoints
                    mResultTextView.text = barcode.displayValue

                    Thread{
                        sendGet(barcode.displayValue)

                        //   runOnUiThread({
                        //        //Update UI
                        //     })
                    }.start()


                } else
                    mResultTextView.setText(R.string.no_barcode_captured)
            } else
                Log.e(LOG_TAG, String.format(getString(R.string.barcode_error_format),
                        CommonStatusCodes.getStatusCodeString(resultCode)))
        } else
            super.onActivityResult(requestCode, resultCode, data)
    }

    companion object {
        private val LOG_TAG = MainActivity::class.java.simpleName
        private val BARCODE_READER_REQUEST_CODE = 1
    }
}
