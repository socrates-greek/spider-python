package com.example.administrator.myapplication;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.app.Activity;
import android.os.StrictMode;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.example.administrator.myapplication.adapter.MyAdapter;
import com.example.administrator.myapplication.commom.Constants;
import com.example.administrator.myapplication.dao.Article;
import com.scwang.smartrefresh.layout.api.RefreshLayout;
import com.scwang.smartrefresh.layout.listener.OnLoadmoreListener;
import com.scwang.smartrefresh.layout.listener.OnRefreshListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MainActivity extends Activity {
    private ListView listview;
    private MyAdapter mAdapter;
    private List<Article> data;
    private Article item;
    private boolean DEV_MODE = true;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        if (DEV_MODE) {
            StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder()
                    .detectCustomSlowCalls() //API等级11，使用StrictMode.noteSlowCode
                    .detectDiskReads()
                    .detectDiskWrites()
                    .detectNetwork()   // or .detectAll() for all detectable problems
                    .penaltyDialog() //弹出违规提示对话框
                    .penaltyLog() //在Logcat 中打印违规异常信息
                    .penaltyFlashScreen() //API等级11
                    .build());
            StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder()
                    .detectLeakedSqlLiteObjects()
                    .detectLeakedClosableObjects() //API等级11
                    .penaltyLog()
                    .penaltyDeath()
                    .build());
        }

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getData();//填充数据
        listview = (ListView) findViewById(R.id.listviewId);
        //设定列表项的选择模式为单选
        listview.setChoiceMode(ListView.CHOICE_MODE_SINGLE);
        //为数据绑定适配器
        mAdapter = new MyAdapter(this,data);
        listview.setAdapter(mAdapter);



        //下拉刷新作用
        RefreshLayout refreshLayout = (RefreshLayout)findViewById(R.id.refreshLayout);
        refreshLayout.setOnRefreshListener(new OnRefreshListener() {
            @Override
            public void onRefresh(RefreshLayout refreshlayout) {
                refreshlayout.finishRefresh(1500);
                getData();
                mAdapter.refresh(data);
            }
        });
        refreshLayout.setOnLoadmoreListener(new OnLoadmoreListener() {
            @Override
            public void onLoadmore(RefreshLayout refreshlayout) {
                refreshlayout.finishLoadmore(1500);
            }
        });




        //添加点击事件
        listview.setOnItemClickListener(new AdapterView.OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
                //获得选中项的HashMap对象
                Article map= (Article)listview.getItemAtPosition(arg2);
                item = map;
                mAdapter.notifyDataSetChanged();
                Long ID = item.getId();
                try {
                    String result= ServiceUtil.getServiceInfo(Constants.ArticleById+ID,Constants.ip,Constants.port);
                    JSONObject jsonObject = new JSONObject(result);
                    String title = jsonObject.getString("title");
                    String detail = jsonObject.getString("detail");
                    Intent i = new Intent(MainActivity.this, ScrollingActivity.class);
                    //用Bundle携带数据
                    Bundle bundle=new Bundle();
                    //传递name参数为tinyphp
                    bundle.putString("content", detail);
                    bundle.putLong("id", ID);
                    bundle.putString("title", title);
                    i.putExtras(bundle);
                    startActivity(i);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }

        });


        /*
         * 方法二：独立类实现button实现,阅读按钮
         */
        Button btn2 = (Button) findViewById(R.id.button8);
        btn2.setOnClickListener(new btn2Click(this));

    }

    private void getData(){
        data=new ArrayList<Article>();

        try {
            String result= ServiceUtil.getServiceInfo(Constants.ArticleTitleList,Constants.ip,Constants.port);
            JSONArray jsonArray = new JSONArray(result);
            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                String title = jsonObject.getString("title");
                Long id = Long.valueOf(jsonObject.getString("id"));
                Article article = new Article();
                article.setId(id);
                article.setTitle(title);
                data.add(article);
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
                    Long ID = item.getId();
                    try {
                        String result= ServiceUtil.getServiceInfo(Constants.ArticleById+ID,Constants.ip,Constants.port);
                        JSONObject jsonObject = new JSONObject(result);
                        String title = jsonObject.getString("title");
                        String detail = jsonObject.getString("detail");

                        Intent i = new Intent(MainActivity.this, ScrollingActivity.class);
                        //用Bundle携带数据
                        Bundle bundle=new Bundle();
                        //传递name参数为tinyphp
                        bundle.putString("content", detail);
                        bundle.putString("title", title);
                        bundle.putLong("id", ID);

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
