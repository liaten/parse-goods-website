<?php
    require_once('configuration.php');

    $fr_name = './result.json';
    $file_read = file($fr_name);

    $time = time();
    $date = date('Y-m-d H:i:s',$time);
    $gmdate = gmdate('Y-m-d H:i:s',$time);

    $json = (json_decode($file_read[0],true));
    $name = $json["name"];
    $description = $json["desctiption"];
    $rating = array_key_exists("rating",$json)? $json["rating"]:null;
    $product_sold = array_key_exists("product_sold",$json)? $json["product_sold"]:null;
    $product_count = array_key_exists("product_count",$json)? $json["product_count"]:null;
    $options = $json["options"];
    $url = $json["url"];
    $image_local_url = $json["image_local_url"];
    $options_str = "";
    foreach ($options as $option => $value){
        $options_str.=($option."\n");
        $v_counter = 0;
        foreach ($value as $v){
            $v_counter++;
            $options_str.=($v_counter.": ".$v."\n");
        }
    }
    // print($options_str);
    $perestanovki = $json["perestanovki"];
    $p_counter = 0;
    $p_str = "";
    foreach($perestanovki as $p_key => $p_value){
        $p_counter++;
        $p_str.=("<b>Вариация №".$p_key.":</b>\n");
        foreach($p_value as $key => $value){
            if(is_int($key)){
                $p_str.=($value."\n");
            }
        }
        $p_str.=($p_value["price"]."\n");
        $warehouses = $p_value["warehouses"];
        foreach($warehouses as $w_key => $w_value){
            $p_str.=($w_key."\n");
            foreach($w_value as $key => $value){
                $p_str.=($value."\n");
            }
        }
    }
    // print($p_str);
    $html = "";
    $html .= "<img src=\"".$image_local_url."\" alt=".$name." class=\"img_center\">";
    if($rating!=null){
        $html .= "<b>Рейтинг: </b>".$rating;
    }
    if($product_sold!=null){
        $html .= "<b>Продано: </b>".$product_sold;
    }
    if($product_count!=null){
        $html .= "\n<b>Всего товара: </b>".$product_count;
    }
    $html .= "\n<b>Опции</b>\n".$options_str;
    $html .= $p_str;
    $html .= "<b>Описание</b>\n".$description;
    $html = mysqli_real_escape_string($con,$html);
    

        $sql = 'INSERT INTO wp_posts
        (
            post_author,
            post_date,
            post_date_gmt,
            post_content,
            post_title,
            post_excerpt,
            post_status,
            comment_status,
            ping_status,
            post_password,
            post_name,
            to_ping,
            pinged,
            post_modified,
            post_modified_gmt,
            post_content_filtered,
            post_parent,
            guid,
            menu_order,
            post_type,
            post_mime_type,
            comment_count
        )
        VALUES (
                    1, # post_author bigint
                    "'.$date.'", # post_date datetime
                    "'.$gmdate.'", # post_date_gmt datetime
                    "'.$html.'", # post_content longtext
                    "'.$name.'", # post_title text
                    "", # post_excerpt text
                    "publish", # post_status varchar(20)
                    "open", # comment_status varchar(20)
                    "open", # ping_status varchar(20)
                    "", # post_password varchar(255)
                    "'.$name.'", # post_name varchar(200)
                    "", # to_ping text
                    "", # pinged text
                    "'.$date.'", # post_modified datetime
                    "'.$gmdate.'", # post_modified_gmt datetime
                    "", # post_content_filtered longtext
                    0, # post_parent bigint
                    "https://liaten.ru/?p=1", # guid varchar(255)
                    "0", # menu_order int
                    "post", # post_type varchar(20)
                    "", # post_mime_type varchar(100)
                    0  # comment_count bigint
                )';
        $response = array();
        if(mysqli_query($con, $sql)){
            $response['success']=true;
            $response['type']='insert_post';
        }
        else{
            $response['success']=false;
            $response['sql'] = $sql;
            $response['error_message'] = mysqli_error($con);
        }
        echo json_encode($response, JSON_UNESCAPED_UNICODE);
?>