{
    debug
    http_port <EXPOSED_PORT>
    http_port 80
    auto_https disable_redirects
}

:80 {
    reverse_proxy * :<EXPOSED_PORT>
}

:<EXPOSED_PORT> {
    reverse_proxy * :8000
    header ForwardTo dqserv
}

:<EXPOSED_PORT>/dqurl* {
    uri strip_prefix /dqurl
    reverse_proxy * 127.0.0.1:80
}

:<EXPOSED_PORT>/static* {
    uri strip_prefix /static
    rewrite /static/ /

    file_server
    root * <DQAPP>/static_root
}

:<EXPOSED_PORT>/cms* {
    redir /cms/admin /cms/admin/
    redir /cms/admin/ /cms/wp-admin/

    uri strip_prefix /cms
    redir /cms /cms/
    rewrite /cms/ /

    file_server
    root * <WORDPRESS_PATH>

    # socket for production, port for debug
    php_fastcgi unix//run/php/php.sock
    # php_fastcgi 127.0.0.1:9000
}
