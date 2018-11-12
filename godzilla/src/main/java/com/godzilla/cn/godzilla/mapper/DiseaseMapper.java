package com.godzilla.cn.godzilla.mapper;

import com.godzilla.cn.godzilla.bean.Article;
import com.godzilla.cn.godzilla.bean.Disease;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface DiseaseMapper {

    @Select("select t.kid, t.id,t.dname,t.symName,t.esymName,t.dtype,t.ditype,#{id} as pid from temp t where LENGTH(t.id) = #{le} and t.id like CONCAT(#{id}, '%')")
    List<Disease> findLists(@Param("id") String id, @Param("le") Long  le);

    @Select("select t.kid, t.id,t.dname,t.symName,t.esymName,t.dtype,t.ditype,'' as pid from temp t where LENGTH(t.id) = #{le} ")
    List<Disease> findFirstLists( @Param("le") Long  le);

    @Update("UPDATE temp SET pid = #{pid} WHERE kid = #{kid}")
    int update(@Param("pid") String pid, @Param("kid") long kid);

}
