package com.example.administrator.myapplication;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import android.annotation.SuppressLint;
import android.os.StrictMode;
import android.util.Log;

@SuppressLint("NewApi")
public class ServiceUtil {
    public static String userAgent =  "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36";
    public static String getServiceInfo  (String strUrl,String ip,String port)
    {
        System.setProperty("https.proxyHost", ip);
        System.setProperty("https.proxyPort", port);
        StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder().detectDiskReads().detectDiskWrites().detectNetwork().penaltyLog().build());
        StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder().detectLeakedSqlLiteObjects().detectLeakedClosableObjects().penaltyLog().penaltyDeath().build());
        HttpURLConnection conn = null;
        BufferedReader reader = null;
        String rs = null;
        try {
            StringBuffer sb = new StringBuffer();
            URL url = new URL(strUrl);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-agent", userAgent);
            conn.setUseCaches(false);
            conn.setConnectTimeout(90000);
            conn.setReadTimeout(90000);
            conn.setInstanceFollowRedirects(false);
            conn.connect();

            InputStream is = conn.getInputStream();
            reader = new BufferedReader(new InputStreamReader(is, "UTF-8"));
            String strRead = null;
            while ((strRead = reader.readLine()) != null) {
                sb.append(strRead);
            }
            rs = sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if (conn != null) {
                conn.disconnect();
            }
        }
        if(null!=rs){
            rs = rs;
        }
        return rs;
    }

    /**
     * post请求获取数据
     * @param strUrl 请求地址，如： "http://....asmx/HelloWork"
     * @param params 设置发送的参数，如："key=1&name=1";//设置发送的参数
     * @return
     */
    public static String getServiceInfoPost(String strUrl,String params)
    {
        String strResult="";
        try{

            byte[] entity = params.getBytes();
            HttpURLConnection con = (HttpURLConnection) new URL(strUrl).openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true);
            con.setConnectTimeout(90000);
            con.setReadTimeout(90000);
            con.setRequestProperty("Content-Type","application/x-www-form-urlencoded");
            con.setRequestProperty("Content-Length",String.valueOf(entity.length));
            con.getOutputStream().write(entity);
            int code =con.getResponseCode();//响应代码 200表示成功
            if(code==200){
                InputStream inStream = con.getInputStream();
                strResult=new String(readInputStream(inStream), "UTF-8");
                if(null!=strResult){
                    strResult = strResult.replace( "<boolean xmlns=\"http://tempuri.org/\">", "")
                            .replace("</boolean>", "")
                            .replace("</string>", "").replace("\r", "")
                            .replace("\n", "")
                            .replace("<string xmlns=\"http://tempuri.org/\" />", "");
                }
            }
        }
        catch(Exception ex){
            Log.e("getServiceInfoPost",ex.getMessage());
        }
        return strResult;
    }

    /**
     * 从输入流中读取数据
     * @param inStream
     * @return
     * @throws Exception
     */
    public static byte[] readInputStream(InputStream inStream) {
        try{
            ByteArrayOutputStream outStream = new ByteArrayOutputStream();
            byte[] buffer = new byte[10000];
            int len = 0;
            while( (len = inStream.read(buffer)) !=-1 ){
                outStream.write(buffer, 0, len);
            }
            byte[] data = outStream.toByteArray();//网页的二进制数据
            outStream.close();
            inStream.close();
            return data;
        }
        catch(Exception ex){
            return null;
        }
    }

}