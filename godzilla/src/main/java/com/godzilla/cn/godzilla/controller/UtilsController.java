package com.godzilla.cn.godzilla.controller;


import com.alibaba.fastjson.JSON;
import com.godzilla.cn.godzilla.bean.Disease;
import com.godzilla.cn.godzilla.bean.Drug;
import com.godzilla.cn.godzilla.bean.Notes;
import com.godzilla.cn.godzilla.service.DiseaseService;
import com.godzilla.cn.godzilla.service.NotesService;
import com.godzilla.cn.godzilla.utils.SignUtil;
import com.google.common.hash.Hashing;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;
import io.swagger.annotations.ApiOperation;
import mjson.Json;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping(value="/utils")     // 通过这里配置使下面的映射都在/users下，可去除
public class UtilsController {


    @Autowired
    public NotesService notesService;

    @Autowired
    public DiseaseService diseaseService;


    @ApiOperation(value="生成hash256", notes="")
    @GetMapping(value="/getHash256")
    public String findNotesByUserId(@RequestParam(value = "queryStr") String queryStr) {

        String path = Hashing.sha256().hashBytes(queryStr.getBytes()).toString();

        return path;
    }

    @ApiOperation(value="生成请求签名", notes="生成请求签名")
    @GetMapping(value="/getSign")
    public String getSign(@RequestParam(value = "queryStr") String queryStr,@RequestParam(value = "clientSecret") String clientSecret) {
        String sign = SignUtil.getSign(queryStr,clientSecret);
        return sign;
    }


    @ApiOperation(value="运算疾病生成同义词目录", notes="运算生成同义词目录")
    @GetMapping(value="/getSymnon")
    public String getSign(@RequestParam(value = "le") Long le,@RequestParam(value = "id") String id) {
        List<Disease> diseases = new ArrayList<>();
        List<Disease> lists = diseaseService.findFirstLists(le);
        for (int i=0;i<lists.size();i++){
            Disease  disease = lists.get(i);
            String id1 = disease.getId();
            long kid = disease.getKid();
            diseases.add(disease);
            //二级的资源
            List<Disease> lis2  = diseaseService.findLists(id1,7L);
            detail(diseases,lis2, kid, 11L);
        }

        System.out.println("大小"+diseases.size());
        diseases.stream().forEach(item->{
            String pid = item.getPid();
            long did = item.getKid();
            if (org.apache.commons.lang3.StringUtils.isNotBlank(pid)){
                diseaseService.update(pid,did);
            }

        });
        return JSON.toJSONString("可以");
    }


    public void detail(List<Disease> diseases,List<Disease> lis, long pid,Long l){
        for (int n=0;n<lis.size();n++){
            Disease  disease = lis.get(n);
            disease.setPid(String.valueOf(pid));
            diseases.add(disease);
            String id = disease.getId();
            long kid = disease.getKid();
            List<Disease> nodelist  = diseaseService.findLists(id,l);
            if (nodelist.size()>0){
                detail(diseases,nodelist,kid,l+4);
            }else{
                //
            }
        }
    }


    @ApiOperation(value="运算药品生成同义词目录", notes="运算生成同义词目录")
    @GetMapping(value="/getDrug")
    public String getDrug() {
        List<Drug> drugs = new ArrayList<>();
        List<Drug> lists = diseaseService.findFirstLists();
        for (int i=0;i<lists.size();i++){
            Drug  drug = lists.get(i);
            long pid = drug.getId();
            if (i<10){
                drug.setGg("M000"+i);
            }else{
                drug.setGg("M00"+i);
            }
            drugs.add(drug);
            //二级的资源
            List<Drug> lis2  = diseaseService.findLists(String.valueOf(pid));
            if (lis2.size()>0){
                detail(drugs,lis2,drug.getGg());
            }
//            int n=100;
//            for (int j=0;j<lis2.size();j++){
//                Drug  drug2 = lis2.get(i);
//                long pid2 = drug2.getId();
//                drug2.setGg(drug.getGg()+n);
//                n++;
//                List<Drug> lis3  = diseaseService.findLists(String.valueOf(pid2));
//
//                int m=100;
//                for (int k=0;k<lis3.size();k++){
//                    Drug  drug3 = lis3.get(i);
//                    long pid3 = drug3.getId();
//                    drug3.setGg(drug2.getGg()+m);
//                    m++;
//                    List<Drug> lis4  = diseaseService.findLists(String.valueOf(pid3));
//
//                }
//
//            }
        }

        drugs.stream().forEach(item->{
            diseaseService.updateDrug(item.getGg(),item.getId());
        });

        return JSON.toJSONString("可以");
    }



    public void detail(List<Drug> drugs,List<Drug> lis3, String gg){

        int m=100;
        for (int k=0;k<lis3.size();k++){
            Drug  drug3 = lis3.get(k);
            long pid3 = drug3.getId();
            if (k<10){
                drug3.setGg(gg+".0000"+k);
            }else if (k>=10 && k<100){
                drug3.setGg(gg+".000"+k);
            }else if(k>=100 && k<1000){
                drug3.setGg(gg+".00"+k);
            }else if(k>=1000 && k<10000){
                drug3.setGg(gg+".0"+k);
            }else{
                drug3.setGg(gg+"."+k);
            }
            drugs.add(drug3);
            m++;
            List<Drug> lis4  = diseaseService.findLists(String.valueOf(pid3));
            if (lis4!=null && lis4.size()>0){
                detail(drugs,lis4,drug3.getGg());
            }else{
                //
            }

        }

    }
}
