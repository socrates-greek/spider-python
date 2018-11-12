package com.godzilla.cn.godzilla.mapper;

import com.godzilla.cn.godzilla.bean.Disease;
import com.godzilla.cn.godzilla.bean.Drug;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface DrugMapper {

    @Select("select p.id,p.aa,p.bb,p.cc,p.dd,p.ee,p.ff,p.gg from temp_2 p  where p.ff = #{ff}")
    List<Drug> findLists(@Param("ff") String ff);

    @Select("select p.id,p.aa,p.bb,p.cc,p.dd,p.ee,p.ff,p.gg from temp_2 p  where p.ff is null")
    List<Drug> findFirstLists();

    @Update("UPDATE temp_2 SET gg = #{pid} WHERE id = #{id}")
    int updateDrug(@Param("pid") String pid, @Param("id") long kid);

}
