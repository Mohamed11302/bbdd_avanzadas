<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions">
    
    <!-- Template para formatear la fecha -->
    <xsl:template name="formatDate">
        <xsl:param name="timestamp"/>
        <p>
            <strong>Fecha: </strong> 
            <xsl:value-of select="fn:format-dateTime(fn:adjust-dateTime-to-timezone(xs:dateTime('1970-01-01T00:00:00') + xs:dayTimeDuration('PT' || $timestamp || 'S')), '[D01]/[M01]/[Y0001]')"/>
        </p>
        <p>
            <strong>Hora: </strong> 
            <xsl:value-of select="fn:format-dateTime(fn:adjust-dateTime-to-timezone(xs:dateTime('1970-01-01T00:00:00') + xs:dayTimeDuration('PT' || $timestamp || 'S')), '[H01]:[m01]')"/>
        </p>
    </xsl:template>

    <!-- Template para el elemento raíz 'data' -->
    <xsl:template match="data">
        <html>
            <head>
                <title>XML EssalhiGalán</title>
                <style>
                    /* Estilos CSS para mejorar la presentación */
                    body {
                        font-family: Arial, sans-serif;
                    }
                    .document {
                        border: 1px solid #ccc;
                        margin-bottom: 20px;
                        padding: 10px;
                    }
                    h1 {
                        text-align: center;
                    }
                    h2 {
                        margin-top: 0;
                    }
                    .answer {
                        margin-left: 20px;
                    }
		    .half-separator {
       		 	border-top: 1px dashed #000;
        		width: 30%;
    		    }
		    .content-description {
        		font-size: 1.17em; /* Tamaño de fuente equivalente al de h3 */
       		 	font-weight: normal; /* Sin negrita */
    		    }
                </style>
            </head>
            <body>
                <h1>XML EssalhiGalán</h1>
                <!-- Aplicar plantilla para cada elemento 'document' -->
                <xsl:apply-templates select="document"/>
            </body>
        </html>
    </xsl:template>

    <!-- Template para el elemento 'document' -->
    <xsl:template match="document">
        <div class="document">
            <h2>
                <xsl:value-of select="subject"/>
            </h2>
	    <p class="content-description">
                <xsl:value-of select="content"/>
            </p>
	    <div class="half-separator"></div>
	    <p>
                <strong>Id Usuario: </strong> 
                <xsl:for-each select="id">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>
            </p>
	    <p>
                <strong>Lenguaje: </strong> 
                <xsl:for-each select="qlang">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>
            </p>  
	    <p>
                <strong>Localización: </strong> 
                <xsl:for-each select="qintl">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>
            </p>
	    <div class="half-separator"></div>
	    <p>
                <strong>Categoria principal: </strong> 
                <xsl:for-each select="maincat">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>
            </p>
	    <p>
                <strong>Categoría: </strong> 
                <xsl:for-each select="cat">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>
            </p>
            <p>
                <strong>Subcategoría: </strong> 
                <xsl:for-each select="subcat">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>
            </p>
            <div class="half-separator"></div>
            <xsl:call-template name="formatDate">
                <xsl:with-param name="timestamp" select="date"/>
            </xsl:call-template>
            <div class="half-separator"></div>
            
<p>
    <h3>Mejor respuesta <br /></h3> 
    <p><strong>Autor: </strong> 
    <xsl:for-each select="best_id">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">, </xsl:if>
                </xsl:for-each>   
    </p>
    <xsl:value-of select="fn:replace(fn:replace(bestanswer, '&#60;br /&#62;', '&#10;'), '&#60;br&#47;&#62;', '&#10;')"/>
</p>


            <h3>Otras respuestas:</h3>
            <ul>
                <!-- Aplicar plantilla para cada elemento 'answer_item' dentro de 'nbestanswers' -->
                <xsl:apply-templates select="nbestanswers/answer_item"/>
            </ul>
            <br />
        </div>
    </xsl:template>

    <!-- Template para el elemento 'answer_item' -->
    <xsl:template match="answer_item">
        <li class="answer">
            <xsl:value-of select="fn:replace(fn:replace(., '&#60;br /&#62;', '&#10;'), '&#60;br&#47;&#62;', '&#10;')"/>
        </li>
        <br />
    </xsl:template>
</xsl:stylesheet>
