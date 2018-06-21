package com.example.administrator.myapplication;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.support.annotation.NonNull;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.app.LoaderManager.LoaderCallbacks;

import android.content.CursorLoader;
import android.content.Loader;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;

import android.os.Build;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.text.TextUtils;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.administrator.myapplication.commom.Constants;
import com.example.administrator.myapplication.dao.User;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import static android.Manifest.permission.READ_CONTACTS;

/**
 * A login screen that offers login via email/password.
 */
public class LoginActivity extends Activity{

    private EditText id_login;
    private EditText password_login;
    private ImageView avatar_login;
    private CheckBox rememberpassword_login;
    private CheckBox auto_login;
    private Button button_login;
    private SharedPreferences sp;
    private String idvalue;
    private String passwordvalue;
    private static final int PASSWORD_MIWEN = 0x81;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        sp = this.getSharedPreferences("userInfo", Context.MODE_PRIVATE);
        //找到相应的布局及控件
        setContentView(R.layout.activity_login);
        id_login=(EditText) findViewById(R.id.login_id);
        password_login=(EditText) findViewById(R.id.login_password);
        avatar_login=(ImageView) findViewById(R.id.login_avatar);
        rememberpassword_login=(CheckBox) findViewById(R.id.login_rememberpassword);
        auto_login=(CheckBox) findViewById(R.id.login_autologin);
        button_login=(Button) findViewById(R.id.login_button);

        if (sp.getBoolean("ischeck",false)){
            rememberpassword_login.setChecked(true);
            id_login.setText(sp.getString("PHONEEDIT",""));
            password_login.setText(sp.getString("PASSWORD",""));
            //密文密码
            password_login.setInputType(PASSWORD_MIWEN);
            if (sp.getBoolean("auto_ischeck",false)){
                auto_login.setChecked(true);

                try {
                    User user =new User();
                    user.setCount(id_login.getText().toString());
                    user.setPassword(password_login.getText().toString());
                    JSONObject jsonObj = new JSONObject();
                    jsonObj.put("count",id_login);
                    jsonObj.put("password",password_login);
                    ServiceUtil serviceUtil = new ServiceUtil();
                    String result= serviceUtil.getServiceInfoPost(Constants.UserByCountAndPassword,jsonObj.toString());
                    if (result.length()>1){
                        Intent i = new Intent(LoginActivity.this, MainActivity.class);
                        startActivity(i);
                    }else{
                        Toast.makeText(LoginActivity.this, "手机号码或密码错误，请重新登录", Toast.LENGTH_SHORT).show();

                    }

                } catch (JSONException e) {
                    e.printStackTrace();
                }
//                Intent intent = new Intent(MainActivity.this,SecondActivity.class);
//                startActivity(intent);
            }
        }

        button_login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                id_login.getPaint().setFlags(0);
                idvalue=id_login.getText().toString();
                password_login.getPaint().setFlags(0);
                passwordvalue=password_login.getText().toString();

                if (!idvalue.equals("") && !passwordvalue.equals("")){

                    if (rememberpassword_login.isChecked()){
                        SharedPreferences.Editor editor=sp.edit();
                        editor.putString("PHONEEDIT",idvalue);
                        editor.putString("PASSWORD",passwordvalue);
                        editor.commit();
                    }
                    try {
                        User user =new User();
                        user.setCount(id_login.getText().toString());
                        user.setPassword(password_login.getText().toString());
                        JSONObject jsonObj = new JSONObject();
                        jsonObj.put("count",idvalue);
                        jsonObj.put("password",passwordvalue);
                        ServiceUtil serviceUtil = new ServiceUtil();
                        String result= serviceUtil.getServiceInfoPost(Constants.UserByCountAndPassword,jsonObj.toString());
                        if (result.length()>1){
                            Intent i = new Intent(LoginActivity.this, MainActivity.class);
                            Bundle bundle=new Bundle();
                            //传递name参数为tinyphp
                            bundle.putString("userId", idvalue);
                            i.putExtras(bundle);
                            startActivity(i);
                        }else{
                            Toast.makeText(LoginActivity.this, "手机号码或密码错误，请重新登录", Toast.LENGTH_SHORT).show();
                        }

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }else{
                    Toast.makeText(LoginActivity.this, "手机号码或密码错误，请重新登录", Toast.LENGTH_SHORT).show();
                }
            }
        });

        rememberpassword_login.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (rememberpassword_login.isChecked()){
                    System.out.println("记住密码已选中");
                    sp.edit().putBoolean("ischeck",true).commit();
                }
                else {
                    System.out.println("记住密码没有选中");
                    sp.edit().putBoolean("ischeck",false).commit();
                }
            }
        });

        auto_login.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (auto_login.isChecked()){
                    System.out.println("自动登录已选中");
                    sp.edit().putBoolean("auto_ischeck",true).commit();
                }else {
                    System.out.println("自动登录没有选中");
                    sp.edit().putBoolean("auto_ischeck",false).commit();
                }
            }
        });
    }

}