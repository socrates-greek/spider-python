package com.example.administrator.myapplication;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.example.administrator.myapplication.dao.Article;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MainActivity extends Activity {
    private ListView listview;
    private ArrayAdapter adapter;
    private List<String> data;
    private String item;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getData();//填充数据
        listview = (ListView) findViewById(R.id.listviewId);
        //设定列表项的选择模式为单选
        adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_activated_1,data);
        listview.setChoiceMode(ListView.CHOICE_MODE_SINGLE);
        listview.setAdapter(adapter);
        listview.isOpaque();
        //添加点击事件
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
                //获得选中项的HashMap对象
                String map= (String)listview.getItemAtPosition(arg2);
                item = map;
            }

        });


        /*
         * 方法二：独立类实现button实现,阅读按钮
         */
        Button btn2 = (Button) findViewById(R.id.button8);
        btn2.setOnClickListener(new btn2Click(this));

    }

    private void getData(){
        data=new ArrayList<String>();

        try {
            String result= ServiceUtil.getServiceInfo("http://192.168.2.182:8080/article/getArticleTitleList","192.168.2.182","8080");
            JSONArray jsonArray = new JSONArray(result);
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String title = jsonObject.getString("title");
                Long id = Long.valueOf(jsonObject.getString("id"));

                data.add(title+"-"+id);
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }
    }



    public class btn2Click implements View.OnClickListener {

        private Context context;

        //重载btn2Click方法
        public btn2Click(Context ct) {
            this.context = ct;
        }
        @Override
        public void onClick(View v) {
            switch (v.getId()) {
                case R.id.button8:
                    String id = item.split("-")[1];
                    Long ID = Long.valueOf(id);
                    try {
                        String result= ServiceUtil.getServiceInfo("http://192.168.2.182:8080/article/getArticle/"+ID,"192.168.2.182","8080");
                        JSONObject jsonObject = new JSONObject(result);
                        String title = jsonObject.getString("title");
                        String detail = jsonObject.getString("detail");

                        Intent i = new Intent(MainActivity.this, ScrollingActivity.class);
                        //用Bundle携带数据
                        Bundle bundle=new Bundle();
                        //传递name参数为tinyphp
                        bundle.putString("content", detail);
                        i.putExtras(bundle);
                        startActivity(i);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


                    break;
                default:
                    Toast tot2 = Toast.makeText(
                            context,
                            "独立类实现button",
                            Toast.LENGTH_LONG);
                    tot2.show();

            }

        }

    }
}
